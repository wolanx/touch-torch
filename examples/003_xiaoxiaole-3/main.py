from pprint import pprint

import numpy as np

from files.xxl_algo import xxl_find_actions, xxl_rec_rect


def do_move(ctx):
    cropMain = {"unit": "%", "x": 0, "y": 20, "width": 100, "height": 60}

    colorR = T.findImg("red.png", crop=cropMain)
    colorG = T.findImg("green.png", crop=cropMain)
    colorB = T.findImg("blue.png", crop=cropMain)
    colorY = T.findImg("yellow.png", crop=cropMain)
    color5 = T.findImg("brown.png", crop=cropMain)
    # color6 = 紫色、五彩鸟、特效鸟等 todo

    # 找出所有的方块，得出行列数
    rects = xxl_rec_rect(T.getScreenshot())
    tb = T.tool.cv2.GridRound(rects)
    rows, cols = tb.getShape()
    print(f"rows={rows} cols={cols}", flush=True)

    # 行列数初始化二维数组
    arr2 = np.zeros((rows, cols), dtype=int)

    # 将颜色(红1绿2蓝3黄4棕5)对应的编号，填入二维数组
    for p in colorR:
        xi, yi = tb.findIdx(p.x, p.y)
        arr2[yi][xi] = 1
    for p in colorG:
        xi, yi = tb.findIdx(p.x, p.y)
        arr2[yi][xi] = 2
    for p in colorB:
        xi, yi = tb.findIdx(p.x, p.y)
        arr2[yi][xi] = 3
    for p in colorY:
        xi, yi = tb.findIdx(p.x, p.y)
        arr2[yi][xi] = 4
    for p in color5:
        xi, yi = tb.findIdx(p.x, p.y)
        arr2[yi][xi] = 5

    # 观察二维数组，调用算法，得到可行的动作
    print(arr2, flush=True)
    actionArr = xxl_find_actions(arr2)
    if len(actionArr) == 0:
        T.log("not found any action")
        return

    T.log("actionArr[0] %s", actionArr[0])
    (iy, ix), action, _ = actionArr[0]
    cx, cy, cw, ch = tb.findRect(ix, iy)
    cx, cy = cx + cw // 2, cy + ch // 2
    cellW, cellH = tb.getCellSize()

    # 根据东南西北 拖拽方块
    match action:
        case "N":
            T.drag(points=[(cx, cy), (cx, int(cy - cellH))], unit="px", duration=0.5)
        case "E":
            T.drag(points=[(cx, cy), (int(cx + cellW), cy)], unit="px", duration=0.5)
        case "S":
            T.drag(points=[(cx, cy), (cx, int(cy + cellH))], unit="px", duration=0.5)
        case "W":
            T.drag(points=[(cx, cy), (int(cx - cellW), cy)], unit="px", duration=0.5)

    T.sleep(1)


T.jobRegister(do_move, cronjob="*", enable=True)


def do_next(ctx):
    T.clickByText(search="继续", crop={"unit": "%", "x": 26, "y": 48, "width": 54, "height": 25})
    T.clickByText(search="开始", crop={"unit": "%", "x": 26, "y": 48, "width": 54, "height": 25})


T.jobRegister(do_next, cronjob="*", enable=True)
