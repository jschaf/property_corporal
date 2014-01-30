from collections import namedtuple
from decimal import Decimal
import xlrd


RowItem = namedtuple('RowItem', ['name', 'parser'])


def split_multi_field(cell_str):
    if cell_str == '':
        return []
    fields = cell_str.split('|')
    values = [None if x == "~" else x for x in fields]
    names = ["serial_number", "detect_serial_number",
             "registration_number", "log", "system_number"]
    assert (len(names) == len(values))
    return zip(names, values)


def get_cell_value(x):
    return None if x == '' else x


def cast_to_int(x):
    return None if x == '' else int(x)


def cast_to_decimal(amount):
    two_places = Decimal(10) ** -2
    if amount == '':
        return None
    else:
        return Decimal(amount).quantize(two_places)


def make_row_parser(header_row):

    row_items = {
        'RECORD TYPE': RowItem('record_type', get_cell_value),
        'LIN': RowItem('line_item_number', get_cell_value),
        'SUBLIN': RowItem('sub_line_item_number', get_cell_value),
        'NSN': RowItem('nsn', get_cell_value),
        'PBIC': RowItem('pbic', get_cell_value),
        'TAC': RowItem('tac', get_cell_value),
        'ERC': RowItem('erc', get_cell_value),
        'ECS': RowItem('ecs', get_cell_value),
        'UIC': RowItem('unit_id_code', get_cell_value),
        'NSN Nomenclature': RowItem('nsn nomenclature', get_cell_value),
        'REQ': RowItem('mtoe_required', cast_to_int),
        'AUTH': RowItem('authorized', cast_to_int),
        'OH': RowItem('on-hand', cast_to_int),
        'DI': RowItem('due-in', cast_to_int),
        'DOCUMENT NO': RowItem('document_number', get_cell_value),
        'SC': RowItem('supply_code', get_cell_value),
        'ESD': RowItem('estimated_ship_date', cast_to_int),
        'UI': RowItem('unit_issue', get_cell_value),
        'UP': RowItem('unit_price', cast_to_decimal),
        'RICC': RowItem('reportable_item_control_code', get_cell_value),
        'ECC': RowItem('ecc', get_cell_value),
        'LCC': RowItem('logistics_control_code', get_cell_value),
        'CIIC': RowItem('controlled_item_inventory_code', get_cell_value),
        'AAC': RowItem('aac', get_cell_value),
        'ABA': RowItem('appropriation_budget_activity', get_cell_value),
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
    Parse `file_name` and return a representation.
    """
    last_serial_index = 0
    book = xlrd.open_workbook(file_name)

    # The data is always store on the first sheet of the workbook
    sheet = book.sheet_by_index(0)

    # Reserve some space
    data = [None] * (sheet.nrows - 1)

    header_row = sheet.row(0)

    parse_row = make_row_parser(header_row)
    for row in range(1, sheet.nrows):
        # We start at 0, but the excel sheet starts at 1
        data[row - 1] = parse_row(sheet.row_slice(row))

    return data
