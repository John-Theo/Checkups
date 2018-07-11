import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from time import time


def ocr(list_t, filename, start, mode='show'):
    img = cv2.imread("../img/original/"+filename)
    font = ImageFont.truetype('../fonts/msyhbd.ttf', 14)

    scale_x = img.shape[1] / 1366
    scale_y = img.shape[0] / 768
    scale = max(scale_x, scale_y)
    scale = (1 if scale == 0 else scale)
    # print((int(img.shape[1] / scale_x), int(img.shape[0] / scale_y)))
    img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)))
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)

    # print(img.shape)
    emptyImage = np.zeros(img.shape, np.uint8)
    img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_PIL)

    for texts in list_t:
        str_l = texts[0]
        try:
            str_l = str_l.decode('utf8')
        except AttributeError:
            pass
        position = (int(texts[1][0]/scale), int(texts[1][1]/scale))
        draw.text(position, str_l, font=font, fill=(255, 0, 0))
        # cv2.putText(img, texts[0], texts[1], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    if mode == 'show':
        # cv2.namedWindow("Image")
        cv2.imshow("Image", img)
        cv2.waitKey(0)
    else:
        cv2.IMWRITE_JPEG_QUALITY = 100
        cv2.imwrite("../img/ocr_result/img/"+filename, img)
    end = time()
    print('[ √ ]', filename, 'finished in %.3f s!' % (end-start))
    # cv2.destroyAllWindows()
