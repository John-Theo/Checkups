from aip import AipOcr
from src.grapher import ocr
from multiprocessing import Pool, freeze_support, Queue
from src.perspective_correction import wrap
import cv2
from time import time
import os


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


class Img2Txt:
    def __init__(self, txt_folder='../img/ocr_result/txt/', img_folder='../img/original/', if_ocr=True):
        self.txt_folder = txt_folder
        self.img_folder = img_folder
        self.if_ocr = if_ocr

    def do_ocr(self, img, opt, fn, mode):
        def get_client():
            """ 你的 APPID AK SK """
            APP_ID = '10778010'
            API_KEY = 'YFFsficBCr2oUl8IzMlpr8CO'
            SECRET_KEY = 'KKxH7OGvphI70ElfWRdBcKIKqaRhodgq'

            cnt = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            return cnt

        start = time()
        print('[ → ]', fn, 'started...')
        """ 带参数调用通用文字识别（含位置高精度版） """
        client = get_client()

        result = client.general(img, opt)
        print('\t', str(result)[:140]+'...')

        list_t = []
        word_list = []

        for item in result['words_result']:
            pos = item['vertexes_location'][0]
            word = item['words']
            list_t.append((word, (pos['x'], pos['y'])))
            word_list.append(word)

        if self.if_ocr:
            ocr(list_t, fn, start, mode=mode)
        with open(self.txt_folder + fn[:-4] + '.txt', 'w') as f:
            if mode == 'full_info':
                f.write(str(list_t))
            else:
                f.write(''.join(word_list))

        # time.sleep(2)

    def img2txt(self, mode, filename=''):
        def img_size_regulizer(fn):
            img = cv2.imread(self.img_folder + 'wrapped/' + fn)
            if (img.shape[0] > 3000) or (img.shape[1] > 3000):
                print('[ . ] Adjusting size for %s ...' % fn)
                scale_x = img.shape[1] / 3000
                scale_y = img.shape[0] / 3000
                scale = max(scale_x, scale_y)
                img = cv2.resize(img, (int(img.shape[1] / scale), int(img.shape[0] / scale)))
                cv2.imwrite(self.img_folder + fn, img)
                print('[ - ] Adjust finished.')
            return get_file_content(self.img_folder + 'wrapped/' + fn)

        """ 如果有可选参数 """
        options = {}
        options["recognize_granularity"] = "big"
        options["detect_direction"] = "true"
        options["vertexes_location"] = "true"
        options["probability"] = "true"

        print('[ . ] Wrapping for %s ...' % filename)
        warning = wrap(self.img_folder, filename)
        if warning == 'Warp fail':
            print('[ x ] Wrap failed, proceed on.')
        else:
            print('[ - ] Wrap finished.')

        try:
            image = img_size_regulizer(filename)
        except AttributeError:
            print('[ x ] Error in %s' % filename)
            return

        if not os.path.exists(self.txt_folder + filename[:-4] + '.txt'):
            self.do_ocr(image, options, filename, mode)
        else:
            print('[?]  %s already exists!' % (self.txt_folder + filename[:-4] + '.txt'))
        # pool.apply_async(do_ocr, (image, options, filename, mode,))
        # time.sleep(1)

    def batch_preparation(self):

        # pool = Pool(processes=2)

        for i in range(300, 627):
            filename = str(i) + '.jpg'
            self.img2txt(MODE, filename)

        # pool.close()
        # pool.join()


if __name__ == '__main__':
    MODE = 'save'

    freeze_support()
    i2t = Img2Txt(
        txt_folder='../img/categorize/report/ocr_txt/',
        if_ocr=False
    )
    i2t.img2txt(
        filename='28.jpg', mode='full_info'
    )
    # i2t.batch_preparation()
