from typing import List


XLSX_NAME = '帕鲁全配种计算.xlsx'

bread = {}  # 配种合成表
pal = {}  # 帕鲁数据表
pal_name = []   # 帕鲁名字表
breed_detail = {}   # 配种合成表详细

def add_breed_detail(A_no, B_no, C_no):
    if A_no not in breed_detail:
        breed_detail[A_no] = {}
    breed_detail[A_no][B_no] = C_no
    
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
            add_breed_detail(A_name, B_name, cell.value)

    # 打开第5个表 - 帕鲁数据表
    sheet = wb.worksheets[4]
    # 从第二行开始，B列是编号，C列是名字
    for row in sheet.iter_rows(min_row=2, min_col=2):
        if row[0].value is None:
            continue
        pal[str(row[0].value)] = row[1].value
        pal_name.append(row[1].value)

def get_pal_name(no : str):
    """根据编号获取帕鲁名字"""
    if no in pal:
        return pal[no]
    if no in pal_name:
        return no
    import FuzzyWuzzy
    current = ""
    maybe = []
    value = 0
    for name in pal_name:
        v = FuzzyWuzzy.fuzz.ratio(no, name)
        if v > value:
            value = v
            current = name
        if v > 50:
            maybe.append(name)
    if current != "":
        return current
    else:
        if maybe != []:
            raise Exception(f"找不到对应帕鲁，你要找的是不是{maybe}？")
        else:
            raise Exception(f"找不到对应帕鲁。")

############################ COMMAND ############################
cmds = {}
def command(cmd : str, help : str):
    def decorator(func):
        cmds[cmd] = (func, help)
        return func
    return decorator

@command('count_end', '[count_end A] - 计算A的配种方案')
def calc_breed_count(A_no : str):
    """计算有多少种方案能合成该帕鲁"""
    name = get_pal_name(A_no)
    ans = []
    for k , v in bread.items():
        if v == name and (k[1], k[0]) not in ans:
            ans.append(k)
    for a, b in ans:
        print(f"{a} + {b} = {name}")
    print(f"共有{len(ans)}种配种方案能合成{name}")

@command('road', '[road A B] - 计算从A到B的配种方案')
def calc_shortest_breed_road(A_no, B_no):
    """计算从A到B的最短合成路径"""
    A_name = get_pal_name(A_no)
    B_name = get_pal_name(B_no)
    import queue
    ret = []
    min_depth = 9999
    # 使用广度优先搜索
    q = queue.Queue()
    q.put(([A_name]))
    while not q.empty():
        road = q.get()
        now = road[-1]
        for tar in breed_detail[now]:
            if tar == B_name and len(road) <= min_depth:
                # 找到了
                road.append(tar)
                ret.append(road)  
                min_depth = len(road)
            elif tar in road:
                # 往回了，跳过
                continue
            else:
                if len(ret) == 0:
                    # 如果还没找到路径那就继续找，找到了就不再增加新的
                    new_road = road.copy()
                    new_road.append(tar)
                    q.put(new_road)
    for x in ret:
        print(" -> ".join(x))
    print(f"共有{len(ret)}种配种方案能从{A_name}合成{B_name}")

@command("help", "显示帮助")
def help():
    """显示帮助"""
    for cmd in cmds:
        print(cmds[cmd][1])

if __name__ == '__main__':
    include_xlsx()
    while True:
        try:
            cmd = input('请输入命令（帮助请输入help）：')
            args = cmd.split()
            for i in range(len(args)):
                args[i] = args[i].strip()
            if args[0] in cmds:
                cmds[args[0]][0](*args[1:])
            elif args[0] == "exit":
                break
            else:
                print('未知命令')
                help()
        except Exception as e:
            print(e)
    
