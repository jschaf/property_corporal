from collections import namedtuple
from decimal import Decimal
import xlrd

class Propety_Book_Item(object):
    """A representation of one item on a property book.
    """

    def __init__(self, LIN):
        pass
RowItem = namedtuple('RowItem', ['name', 'parser'])

def make_row_parser(header_row):
    get_cell_value = lambda x: None if x == '' else x
    cast_to_int = lambda x: None if x == '' else int(x)
    cast_to_decimal = lambda x: None if x == '' else Decimal(x).quantize(Decimal("0.00"))
    is_multi_field = lambda x: x == 'SER|DETECT SN|REG|LOT|SYS NO'

    def split_multi_field(cell_str):
        if cell_str == '':
            return []
        fields = cell_str.split('|')
        values = [None if x == "~" else x for x in fields]
        names = ["ser", "detect sn", "reg", "log", "sys no"]
        assert(len(names) == len(values))
        return zip(names, values)

    row_items = {
        'RECORD TYPE': RowItem('record type', get_cell_value),
        'LIN': RowItem('lin', get_cell_value),
        'SUBLIN': RowItem('sublin', get_cell_value),
        'NSN': RowItem('nsn', get_cell_value),
        'PBIC': RowItem('pbic', get_cell_value),
        'TAC': RowItem('tac', get_cell_value),
        'ERC': RowItem('erc', get_cell_value),
        'ECS': RowItem('ecs', get_cell_value),
        'UIC': RowItem('uic', get_cell_value),
        'NSN Nomenclature': RowItem('nsn nomenclature', get_cell_value),
        'REQ': RowItem('req', cast_to_int),
        'AUTH': RowItem('auth', cast_to_int),
        'OH': RowItem('oh', cast_to_int),
        'DI': RowItem('di', cast_to_int),
        'DOCUMENT NO': RowItem('document no', get_cell_value),
        'SC': RowItem('sc', get_cell_value),
        'ESD': RowItem('esd', cast_to_int),
        'UI': RowItem('ui', get_cell_value),
        'UP': RowItem('up', Decimal),
        'RICC': RowItem('ricc', get_cell_value),
        'ECC': RowItem('ecc', get_cell_value),
        'LCC': RowItem('lcc', get_cell_value),
        'CIIC': RowItem('ciic', get_cell_value),
        'AAC': RowItem('aac', get_cell_value),
        'ABA': RowItem('aba', get_cell_value),
        'SER|DETECT SN|REG|LOT|SYS NO': "multi-cell"
    }

    row_item_ordered = [row_items[r.value] for r in header_row]

    def row_parser(row):
        item_dict = {}
        for i, cell in enumerate(row):
            row_item = row_item_ordered[i]
            if row_item == "multi-cell":
                item_dict.update(dict(split_multi_field(cell.value)))
            else:
                item_dict[row_item.name] = row_item.parser(cell.value)
        return item_dict

    return row_parser
        
        
def parse_file(file_name):
    """
    Parse `file` and return a representation.
    """
    book = xlrd.open_workbook(file_name)
    sheet = book.sheet_by_index(0)
    # Reserve some space
    data = [None] * sheet.nrows
    for row in range(1, sheet.nrows - 1):
        data[row] = sheet.row_slice(row)
