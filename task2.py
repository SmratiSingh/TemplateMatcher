"""
Character Detection
(Due date: March 8th, 11: 59 P.M.)

The goal of this task is to experiment with template matching techniques. Specifically, the task is to find ALL of
the coordinates where a specific character appears using template matching.

There are 3 sub tasks:
1. Detect character 'a'.
2. Detect character 'b'.
3. Detect character 'c'.

You need to customize your own templates. The templates containing character 'a', 'b' and 'c' should be named as
'a.jpg', 'b.jpg', 'c.jpg' and stored in './data/' folder.

Please complete all the functions that are labelled with '# TODO'. Whem implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in utils.py
and the functions you implement in task1.py are of great help.

Hints: You might want to try using the edge detectors to detect edges in both the image and the template image,
and perform template matching using the outputs of edge detectors. Edges preserve shapes and sizes of characters,
which are important for template matching. Edges also eliminate the influence of colors and noises.

Do NOT modify the code provided.
Do NOT use any API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import any library (function, module, etc.).
"""


import argparse
import json
import os

import utils
from task1 import *   # you could modify this line


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img_path", type=str, default="./data/task2.jpg",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--template_path", type=str, default="",
        choices=["./data/a.jpg", "./data/b.jpg", "./data/c.jpg"],
        help="path to the template image")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./results/",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args


def detect(img, template):
    """Detect a given character, i.e., the character in the template image.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        coordinates: list (tuple), a list whose elements are coordinates where the character appears.
            format of the tuple: (x (int), y (int)), x and y are integers.
            x: row that the character appears (starts from 0).
            y: column that the character appears (starts from 0).
    """
    # TODO: implement this function.

    threshold = 0.97
    norm_img = normalize(img)
    norm_template = normalize(template)

    print("image norm ", len(norm_img), len(norm_img[0]))
    print("template norm ", len(norm_template), len(norm_template[0]))

    coordinates = list()
    for i in range(0, len(norm_img)):
        for j in range(0, len(norm_img[0])):
            quo = 0
            sq_img = 0
            sq_temp = 0
            # print("i= ", i)
            # print("j= ", j)
            skip = False
            for k in range(0, len(norm_template)):
                for l in range(0, len(norm_template[0])):
                    # print("k= ", k)
                    # print("l= ", l)
                    a = k + i - 1
                    b = j + l - 1
                    if a >= len(norm_img) or b >= len(norm_img[0]):
                        skip = True
                        # print("python3")
                        break
                    quo += norm_img[a][b] * norm_template[k][l]
                    sq_img += norm_img[a][b] ** 2
                    sq_temp += norm_template[k][l] ** 2
            if not skip:
                normxc = float(quo / np.sqrt(sq_img * sq_temp))
                if normxc >= threshold:
                    flag = True
                else:
                    flag = False

                if flag:
                    coordinate = [i, j]
                    coordinates.append(coordinate)


    # raise NotImplementedError
    return coordinates


def drawResult(img, coordinates, template):
    img_arr = np.asarray(img)
    trlen = len(template) - 1
    tclen = len(template[0]) - 1
    myColor = 0
    print("drawing results for " + str(len(coordinates)) + " detected characters")
    for i in range(len(coordinates)):
            #print(str(i) + " " + str(coordinates[i][0]) + " " + str(coordinates[i][1]) + " " + str(trlen) +" "+str(tclen))
            img_arr = drawRect(coordinates[i][0]-5, coordinates[i][1]-2, img_arr, trlen+5, tclen+5, myColor)

    return img_arr


def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def drawRect(x, y, img, trlen , tclen, myColor):
    for i in range(x, x+trlen):
        if i < len(img):
            img[i][y] = myColor
            img[i][y+tclen] = myColor
    for i in range(y, y+tclen):
        if i < len(img[0]):
            img[x][i] = myColor
            img[x+trlen][i] = myColor
    return img


def main():
    args = parse_args()

    img = read_image(args.img_path)
    template = read_image(args.template_path)

    coordinates = detect(img, template)
    # detect(img, template)

    template_name = "{}.json".format(os.path.splitext(os.path.split(args.template_path)[1])[0])
    save_results(coordinates, template, template_name, args.rs_directory)

    # cv2.imwrite("./results/", drawResult(img, coordinates))
    result = drawResult(img, coordinates, template)
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('image', result)
    cv2.waitKey(100000000)


if __name__ == "__main__":
    main()
