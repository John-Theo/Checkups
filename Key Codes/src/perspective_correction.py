import numpy as np
from imutils import perspective
import cv2
import imutils
import os


def wrap(root, fn):
    wrap_path = (root[:-1] if root[-1] == '/' else root) + '/wrapped/'
    if not os.path.exists(wrap_path):
        os.mkdir(wrap_path)

    # 边缘扫描
    # image = cv2.imread('../img/categorize/report/28.jpg')
    image = cv2.imread((root[:-1] if root[-1] == '/' else root)+'/'+fn)

    ratio = image.shape[0] / 500.0  # 比例
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # 灰度转换及边缘查找
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 50, 200)  # 边缘检测
    # cv2.imshow("Scanned", imutils.resize(edged, height=650))

    # 只保留轮廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 通过边缘图像找到轮廓
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]  # 用以区分OpenCV2.4和OpenCV3
    cnts = sorted(cnts, key=lambda x: cv2.arcLength(x, True), reverse=True)[:5]  # 保留最大轮廓

    # cv2.drawContours(image, [cnts[15]], 0, (0, 0, 255), 2)
    # cv2.imshow("Scanned", imutils.resize(image, height=650))
    # cv2.waitKey(0)

    # 选取上下半图最长线条
    upper_line = [0, 500, 0, 500]
    lower_line = [0, 0, 0, 0]
    for cnt in cnts:
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 2:
            x1, y1, x2, y2 = approx.flat
            if abs(y1 - y2) < image.shape[0] * 0.1:
                if min(y1, y2) > 250:
                    if abs(x1 - x2) > abs(upper_line[0] - upper_line[2]):
                        upper_line = [x1, y1, x2, y2]
                if max(y1, y2) < 250:
                    if abs(x1 - x2) > abs(lower_line[0] - lower_line[2]):
                        lower_line = [x1, y1, x2, y2]

    def adjust_endpoint(l1, l2):
        def x_order(l):
            if l[0] > l[2]:
                l = [l[2], l[3], l[0], l[1]]
            return l
        l1, l2 = x_order(l1), x_order(l2)
        slope_1 = (l1[3] - l1[1]) / (l1[2] - l1[0])
        slope_2 = (l2[3] - l2[1]) / (l2[2] - l2[0])
        if l1[0] < l2[0]:
            l1[0], l1[1] = l2[0], int((l2[0] - l1[0]) * slope_1 + l1[1])
        else:
            l2[0], l2[1] = l1[0], int((l1[0] - l2[0]) * slope_2 + l2[1])
        if l1[2] > l2[2]:
            l1[2], l1[3] = l2[2], int((l1[2] - l2[2]) * slope_1 + l1[3])
        else:
            l2[2], l2[3] = l1[2], int((l2[2] - l1[2]) * slope_2 + l2[3])
        return l1, l2

    try:
        upper_line, lower_line = adjust_endpoint(upper_line, lower_line)
    except ZeroDivisionError:
        cv2.imwrite(wrap_path + fn, orig)
        return 'Warp fail'

    screenCnt = np.array(upper_line+lower_line).reshape(4, 2)

    '''
    Test Code Below
    --------------------------------
    upper_line = np.array([[[upper_line[0], upper_line[1]]], [[upper_line[2], upper_line[3]]]])
    lower_line = np.array([[[lower_line[0], lower_line[1]]], [[lower_line[2], lower_line[3]]]])

    cv2.drawContours(image, [upper_line], 0, (0, 0, 255), 2)
    cv2.drawContours(image, [lower_line], 0, (0, 0, 255), 2)

    for dot in screenCnt:
        cv2.circle(image, (dot[0], dot[1]), 10, (255, 0, 0), -1)
    '''

    # 透视矫正
    warped = perspective.four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    cv2.imwrite(wrap_path+fn, warped)
    return 0


if __name__ == '__main__':
    wrap('../img/categorize/report/', '505.jpg')
