from calc import include_xlsx, breed
from pals_data import Pal

min_breed = {}  # 最低等级配种表


def join_road(r: list, a, b, c: Pal) -> list:
    if (a,b,c) in r or (b,a,c) in r:
        return r
    else:
        return r + [(a, b, c)]


def join_roads(r1: list, r2: list) -> list:
    r = []
    for a, b, c in r1:
        r = join_road(r, a, b, c)
    for a, b, c in r2:
        r = join_road(r, a, b, c)
    return r

def check_and_update(a, b, c):
    level = 10 # 10级以下可以直接获取不需要配种
    old_level, old_road, old_src = min_breed[c][0], min_breed[c][1], min_breed[c][2]
    if old_level <= level:
        return
    # print(f"检查: {a.name} + {b.name} = {c.name} [{c.min_level}]")
    new_level = max(min_breed[a][0], min_breed[b][0])
    new_src = set(min_breed[a][2]) | set(min_breed[b][2])
    new_road = join_roads(min_breed[a][1], min_breed[b][1])
    new_road = join_road(new_road, a, b, c)
    if old_level > level and new_level < old_level:   # 等级超了，需要更新
        min_breed[c] = (new_level, new_road, new_src)
    elif len(new_road) < len(old_road):   # 如果新的需要的步骤更少，更新
        min_breed[c] = (new_level, new_road, new_src)
    elif len(new_road) == len(old_road): # 路径数相同，来源数更少，更新
        if len(new_src) < len(old_src):
            min_breed[c] = (new_level, new_road, new_src)

def iteration():
    """迭代计算最低等级配种表"""
    # 初始化
    if min_breed == {}:
        for a in Pal.all_pals:
            min_breed[a] = (a.min_level, [], {a})
    # 迭代一次所有配方
    for a in Pal.all_pals:
        for b in Pal.all_pals:
            if a.no > b.no:
                continue
            c = breed[(a, b)]
            check_and_update(a, b, c)

cnt = []
def add_cnt(x):
    for c in cnt:
        if c[0] == x:
            c[1] += 1
            return
    cnt.append([x, 1])

def main():
    include_xlsx()
    for i in range(20):
        iteration()
    for x in min_breed:
        if len(min_breed[x][1]) <= 0:
            continue
        print(f"## {x.name}")
        print(f"最低合成等级: {min_breed[x][0]}")
        print()
        print(f"需要以下帕鲁: {', '.join(c.name for c in min_breed[x][2])}:")
        print()
        for c in min_breed[x][2]:
            add_cnt(c)
        if len(min_breed[x][1]) == 0:
            continue
        for l in min_breed[x][1]:
            print(
                f"* {l[0].name} + {l[1].name} = {l[2].name}"
            )
        print()
    print("===========================")
    cnt.sort(key=lambda x: x[1], reverse=True)
    print("源头统计：")
    for x in cnt:
        print(f"* {x[0].name} - {x[1]}")


if __name__ == "__main__":
    # 重定向到文件
    import sys
    sys.stdout = open("min_breed.txt", "w")
    main()
