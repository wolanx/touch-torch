import random
from pprint import pprint

import cv2
import numpy as np


def xxl_rec_rect(img0):
    imgG = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    thBin = cv2.adaptiveThreshold(imgG, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 0)
    thBin = cv2.bitwise_not(thBin)
    edges = cv2.Canny(thBin, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    ret = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 20 or h < 20 or np.abs(w - h) > 10 or w > 900 / 9 or w < (900 / 9) * 0.8:
            continue

        # cv2.rectangle(img0, (x, y), (x + w, y + h), (x % 200, y % 200, 222), 3)
        ret.append((x, y, w, h))

    return ret


def xxl_find_actions(arr2):
    arr2 = np.array(arr2)
    xMax, yMax = arr2.shape
    ret = []

    for cx in range(xMax):
        for cy in range(yMax):
            cv = arr2[cx][cy]

            if cv == 0:
                continue

            # action: N=North E=East S=South W=West
            for dx, dy, action in [(-1, 0, "N"), (0, 1, "E"), (1, 0, "S"), (0, -1, "W")]:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < xMax and 0 <= ny < yMax:
                    match, blocks = xxl_check(arr2, cv, cx, cy, nx, ny)
                    if match:
                        ret.append([(cx, cy), action, blocks])

    random.shuffle(ret)
    return ret


def xxl_check(arr2, pv, px, py, cx, cy):
    xMax, yMax = arr2.shape

    nv = arr2[cx][cy]
    if nv == pv or nv == 0:
        return False, []

    p2Arr = [
        # xxo, xox, oxx
        [(-2, 0), (-1, 0)],
        [(-1, 0), (1, 0)],
        [(1, 0), (2, 0)],
        # yyo, yoy, oyy
        [(0, -2), (0, -1)],
        [(0, -1), (0, 1)],
        [(0, 1), (0, 2)],
    ]

    for (cx1, cy1), (cx2, cy2) in p2Arr:
        nx1, ny1 = cx + cx1, cy + cy1
        nx2, ny2 = cx + cx2, cy + cy2

        if (nx1, ny1) == (px, py) or (nx2, ny2) == (px, py):
            continue

        if 0 <= nx1 < xMax and 0 <= ny1 < yMax and 0 <= nx2 < xMax and 0 <= ny2 < yMax:
            if arr2[nx1][ny1] == pv and arr2[nx2][ny2] == pv:
                return True, [(cx, cy), (nx1, ny1), (nx2, ny2)]

    return False, []
