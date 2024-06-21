import random
from pprint import pprint

import numpy as np


def xxl_find(arr2):
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


# class TestXiaoXiaoLe(unittest.TestCase):
#     def test_1(self):
#         """
#         (0, 1) S
#         (0, 2) W
#         (0, 4) E
#         (0, 5) S
#         (1, 1) E
#         (1, 5) W
#         (2, 2) E
#         (2, 3) N
#         (2, 4) W
#         (5, 3) N
#         """
#         demo = [
#             [0, 1, 4, 0, 4, 1, 0],
#             [1, 4, 1, 3, 1, 4, 1],
#             [1, 4, 4, 1, 4, 4, 1],
#             [0, 1, 2, 3, 2, 1, 0],
#             [0, 0, 1, 4, 1, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0],
#         ]
#         pprint(demo)

#         for one in xxl_find(demo):
#             # pprint(one)
#             (iy, ix), action, _ = one
#             print((iy, ix), action)
