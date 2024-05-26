import copy
import re
from pprint import pprint

from files.sudoku import sudoku_init, sudoku_run


def unname(ctx):
    arr1 = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            # (776 - 120) / 9 = 72
            x = 120 + 72 * j + 6
            y = 384 + 72 * i + 6
            res = T.findText(search="*", crop={"unit": "px", "x": x, "y": y, "width": 66, "height": 72})
            print(res)

            if len(res):
                value = res[0][-1]
                if value == "00":
                    value = "8"
                if value == "07":
                    value = "9"

                # print("set", i, j, value)
                if re.match(r"^\d$", value):
                    arr1[i][j] = int(value)

    pprint(arr1)
    arr2 = copy.deepcopy(arr1)

    x, y = sudoku_init(arr2)
    sudoku_run(arr2, x, y)
    pprint(arr2)

    for i in range(9):
        for j in range(9):
            if arr1[i][j] == 0:
                vInt = arr2[i][j]
                vStr = str(arr2[i][j])
                if vStr == "8":
                    vStr = "00"

                x = 120 + 72 * j + 6 + 72 / 2
                y = 384 + 72 * i + 6 + 72 / 2

                T.click(x=x, y=y, unit="px")
                T.sleep(0.5)

                match vInt:
                    case 1 | 2 | 3:
                        T.clickByText(search=vStr, crop={"unit": "%", "x": 0, "y": 92, "width": 33, "height": 8})
                    case 4 | 5 | 6:
                        T.clickByText(search=vStr, crop={"unit": "%", "x": 33, "y": 92, "width": 33, "height": 8})
                    case 7 | 8 | 9:
                        T.clickByText(search=vStr, crop={"unit": "%", "x": 66, "y": 92, "width": 33, "height": 8})

                T.sleep(0.5)

    T.sleep(30)


T.jobRegister(unname, cronjob="*", enable=True)
