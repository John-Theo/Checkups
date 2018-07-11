# Do NOT delete the next line(disable_warnings)!
import src.side_packages.disable_warning

import cv2
from src.text_classfier import TextClassifier
from src.tf4poets2.my_test_master import CalcResult
from src.img2txt import Img2Txt
import tensorflow as tf
from time import time
import sqlite3
import os
import random


class ClsDataGen:
    def __init__(self, test_f):
        self.test_folder = test_f
        is_exist_dir(self.test_folder)
    
    def img_size_regulizer(self, fn):
        print('---- Adjusting Resolution ----')
        start = time()
        img = cv2.imread(self.test_folder + fn)
        img_reso = cv2.resize(img, (WID_4_CLAFT, int(img.shape[0]/(img.shape[1]/WID_4_CLAFT))))
        cv2.imwrite(self.test_folder+'resolution/' + fn, img_reso)
        print('[ √ ]  Adjusting DONE in %.3f s!' % (time()-start))
    
    def image_classifier(self, fn, dir_prefix=''):
        print('\n---- Classifying as Image ----')
        start = time()
        cr = CalcResult(dir_prefix+'tf4poets2/')
        with tf.Session(graph=cr.graph) as sess:
            result = cr.classify_it(cr.load_tensor(self.test_folder+'resolution/' + fn), sess)
            top_k, labels = cr.meaning_result(result)
        if MODE == 'print':
            for i in top_k:
                print('\t%s [%.3f]' % (labels[i], result[i]))
        print('[ √ ]  Classifying (Image) DONE in %.3f s!' % (time()-start))
        return list(map(lambda x, y: (x, y), labels, result))
    
    def text_classifier(self, fn, dir_prefix=''):
        print('\n---- Classifying as Text ----')
        start = time()
        i2t = Img2Txt(
            txt_folder=self.test_folder+'ocr_txt/',
            img_folder=self.test_folder,
            if_ocr=False
        )
        i2t.img2txt(fn)
        tc = TextClassifier(
            txt_root=self.test_folder+'ocr_'
        )
        result = tc.test_master(fn[:-3]+'txt', 'return', dir_prefix=dir_prefix)
        if MODE == 'print':
            for cls in result:
                print('\t%s [%.3f]' % (cls[0], cls[1]*150))
        print('[ √ ]  Classifying (Text) DONE in %.3f s!' % (time() - start))
        return result


class TestResult:
    def __init__(self, l):
        self.my_dict = {}
        for result in l:
            self.my_dict[result[0]] = result[1]


def is_exist_dir(test_dir):
    for assist_dir in ['resolution', 'ocr_txt']:
        dest_path = test_dir+assist_dir+'/'
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)


# MODE = 'print'
MODE = 'record'
# CHOOSE_METHOD = 'random'
CHOOSE_METHOD = 'everyone'
WID_4_CLAFT = 300

if __name__ == '__main__':
    train_root = '../img/categorize/'
    conn = sqlite3.connect('../db/classification.db')
    c = conn.cursor()

    # for class_ in os.listdir(train_root):
    class_ = 'report'
    cdg = ClsDataGen(train_root+class_+'/')

    if CHOOSE_METHOD == 'random':
        file_list = random.sample(os.listdir(cdg.test_folder), 100)
    else:
        file_list = os.listdir(cdg.test_folder)

    for file_name in file_list:
        c.execute("SELECT * FROM result WHERE file_name='%s'" % file_name)
        if c.fetchone() is not None:
            continue
        print('\n\n------------------------------------------------')
        print('Extracting features from [%s] %s...' % (class_, file_name))
        print('------------------------------------------------\n')

        try:
            cdg.img_size_regulizer(file_name)
            img_clf = TestResult(cdg.image_classifier(file_name))
            txt_clf = TestResult(cdg.text_classifier(file_name))
        except AttributeError:
            print('[ x ] FATAL: Picture not qualified!')
            continue

        result_list = [file_name, class_, 'test']
        for method in ['IMG', 'TXT']:
            for rec_class_ in ['report', 'paper_n_report', 'n_paper']:
                if method == 'IMG':
                    result_list.append(round(img_clf.my_dict[rec_class_]-0, 3))
                else:
                    result_list.append(round(txt_clf.my_dict[rec_class_]-0, 3))

        c.execute("INSERT INTO result VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(result_list))
        conn.commit()

    conn.close()
