from io import BytesIO
from openpyxl import Workbook

def export_excel_file(title, result):
    output = BytesIO()
    write_wb = Workbook()
    write_ws = write_wb.active
    write_ws.append(list(title.values()))
    
    for row in result:
        row_list = []
        for key in title:
            row_list.append(row[key])
        write_ws.append(row_list)
        row_list.clear()

    write_wb.save(output)
    output.seek(0)
    return output