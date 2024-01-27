XLSX_NAME = '帕鲁全配种计算.xlsx'

bread = {}  # 配种合成表
pal = {}  # 帕鲁数据表


def include_xlsx():
    """从xlsx中读取数据"""
    import openpyxl
    wb = openpyxl.load_workbook(XLSX_NAME)
    # 打开第1个表 - 帕鲁配种表
    sheet = wb.worksheets[0]
    # 读取数据
    ## 表格从C3开始
    for row in sheet.iter_rows(min_row=3, min_col=3):
        for cell in row:
            if cell.value is None:
                continue
            column = cell.column
            A_name = sheet.cell(row=2, column=column).value
            B_name = sheet.cell(row=cell.row, column=2).value
            bread[(A_name, B_name)] = cell.value
            bread[(B_name, A_name)] = cell.value
    # 打开第5个表 - 帕鲁数据表
    sheet = wb.worksheets[4]
    # 从第二行开始，B列是编号，C列是名字
    for row in sheet.iter_rows(min_row=2, min_col=2):
        if row[0].value is None:
            continue
        pal[str(row[0].value)] = row[1].value
        
def get_my_pals():
    # 检测是否存在my_pals.py文件，不存在从template复制一个
    import os
    if not os.path.exists('my_pals.py'):
        import shutil
        shutil.copy('my_pals_template.py', 'my_pals.py')
        print('my_pals.py文件不存在，已重新生成。请修改my_pals.py文件后再次运行。')
        exit()
    # 读取my_pals.py文件
    return __import__('my_pals').my_pals


if __name__ == '__main__':
    include_xlsx()
    print(bread)
    print(pal)
