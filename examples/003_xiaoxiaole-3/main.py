from pprint import pprint

import numpy as np

from files.xxl_algo import xxl_find


def unname(ctx):
    # T.drag(points=[(70, 51), (82, 51)], unit="%", duration=0.5)
    # T.sleep(2)

    cropMain = {"unit": "%", "x": 0, "y": 20, "width": 100, "height": 60}

    colorR = T.findImg("red.png", crop=cropMain)
    colorG = T.findImg("green.png", crop=cropMain)
    colorB = T.findImg("blue.png", crop=cropMain)
    colorY = T.findImg("yellow.png", crop=cropMain)
    color5 = T.findImg("brown.png", crop=cropMain)

    print(len(colorR), colorR)
    print(len(colorG), colorG)
    print(len(colorB), colorB)
    print(len(colorY), colorY)
    print(len(color5), color5)

    # for r in res:
    #     points = [(r.x, r.y), (r.x + 50, r.y)]
    #     T.drag(points, unit="px", duration=0.5)
    #     T.sleep(2)

    colorX = colorR + colorG + colorB + colorY
    colX, colY = [one.x for one in colorX], [one.y for one in colorX]
    # 这里偷懒了，可能会有误差。可以手动取点后，计算网格位置
    step = (np.max(colX) - np.min(colX)) / 9
    colX, colY = [int(i // step * step + step / 2) for i in colX], [int(i // step * step + step / 2) for i in colY]  # 正则化误差，将值就近到倍数值上
    colX, colY = np.array(sorted(set(colX))), np.array(sorted(set(colY)))  # 去重，排序

    # 初始化二维数组
    arr2 = [[0 for _ in range(len(colX))] for _ in range(len(colY))]
    # pprint(arr2)

    # 将颜色写入二维数组 红1绿2蓝3黄4棕5
    for p in colorR:
        xi, yi = (np.abs(colX - p.x)).argmin().item(), (np.abs(colY - p.y)).argmin().item()
        arr2[yi][xi] = 1
    for p in colorG:
        xi, yi = (np.abs(colX - p.x)).argmin().item(), (np.abs(colY - p.y)).argmin().item()
        arr2[yi][xi] = 2
    for p in colorB:
        xi, yi = (np.abs(colX - p.x)).argmin().item(), (np.abs(colY - p.y)).argmin().item()
        arr2[yi][xi] = 3
    for p in colorY:
        xi, yi = (np.abs(colX - p.x)).argmin().item(), (np.abs(colY - p.y)).argmin().item()
        arr2[yi][xi] = 4
    for p in color5:
        xi, yi = (np.abs(colX - p.x)).argmin().item(), (np.abs(colY - p.y)).argmin().item()
        arr2[yi][xi] = 5

    pprint(arr2)

    canArr = xxl_find(arr2)
    T.log("canArr %s", canArr)
    (iy, ix), action, _ = canArr[0]
    cx, cy = colX[ix], colY[iy]

    match action:
        case "N":
            T.drag(points=[(cx, cy), (cx, int(cy - step))], unit="px", duration=0.5)
        case "E":
            T.drag(points=[(cx, cy), (int(cx + step), cy)], unit="px", duration=0.5)
        case "S":
            T.drag(points=[(cx, cy), (cx, int(cy + step))], unit="px", duration=0.5)
        case "W":
            T.drag(points=[(cx, cy), (int(cx - step), cy)], unit="px", duration=0.5)

    T.sleep(2)


T.jobRegister(unname, cronjob="*", enable=True)


def go_next(ctx):
    T.clickByText(search="继续", crop={"unit": "%", "x": 26, "y": 48, "width": 54, "height": 25})
    T.sleep(1)


T.jobRegister(go_next, cronjob="*", enable=True)
