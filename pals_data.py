from typing import List, TypeVar

T = TypeVar('T', bound='Pal')

class Pal:
    all_pals : List[T] = []    # 所有帕鲁列表
    def __init__(self):
        self.no = "00"    # 帕鲁编号
        self.name = ""   # 帕鲁名称
        self.power = 0   # 帕鲁繁殖力
        self.min_level = 0   # 帕鲁最低出现等级
        self.max_level = 0   # 帕鲁最高出现等级
    
    def __str__(self) -> str:
        return f"{self.name}({self.power})"
    
    def __repr__(self) -> str:
        return f"[{self.no}]{self.name}（{self.power} {self.min_level}-{self.max_level}）"
    
    @classmethod
    def init(cls):
        import openpyxl
        wb = openpyxl.load_workbook("帕鲁个体数据.xlsx")
        sheet = wb.worksheets[0]
        # id  名称  最小等级  最大等级  繁殖力
        for row in sheet.iter_rows(min_row=2, min_col=1):
            if row[0].value is None:
                continue
            pal = Pal()
            pal.no = str(row[0].value)
            pal.name = row[1].value
            if row[2].value is None:
                pal.min_level = 999
            else:
                pal.min_level = int(row[2].value)
            if row[3].value is None:
                pal.max_level = 999
            else:
                pal.max_level = int(row[3].value)
            pal.power = int(row[4].value)
            cls.all_pals.append(pal)
        # for pal in cls.all_pals:
        #     print(repr(pal))
    
    @classmethod
    def get(cls, no : str) -> T:
        """根据编号获取帕鲁"""
        for pal in cls.all_pals:
            if pal.no == no:
                return pal
        raise Exception(f"找不到对应帕鲁。")
    
    @classmethod
    def get_by_name(cls, name : str) -> T:
        """根据名字获取帕鲁"""
        for pal in cls.all_pals:
            if pal.name == name:
                return pal
        raise Exception(f"找不到对应帕鲁。")