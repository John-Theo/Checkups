import os
from collections import Counter
import json
from random import choices
from datetime import datetime


classes = [
    'n_paper',
    'report',
    'paper_n_report'
]


def print_counter(counter, k=5, title=''):
    for item in counter.most_common(k):
        print(title, item)


class TextClassifier:
    def __init__(self, img_root='../img/train/', txt_root='../img/ocr_result/'):
        self.content_dict = {x: Counter() for x in classes}
        self.img_root = img_root
        self.txt_root = txt_root
        self.dictionary_path = '../img/ocr_result/classify.dictionary'

    def create_dict(self):
        print('Creating words dictionary...')
        for class_ in classes:
            for item in os.listdir(self.img_root+class_+'/'):
                try:
                    with open(self.txt_root+'txt/'+item[:-3]+'txt') as f:
                        self.content_dict[class_].update(list(f.read()))
                except FileNotFoundError:
                    continue
                    # print(item[:-3]+'txt: File NOT FOUND!')

        '''
        Delete most common words appears in all THREE categories.
        '''
        appear_num = Counter()
        for class_ in classes:
            appear_num.update([x[0] for x in self.content_dict[class_].most_common(50)])

        for class_ in classes:
            for item in appear_num.items():
                if item[1] == 3:
                    del self.content_dict[class_][item[0]]
            total_texts = sum(self.content_dict[class_].values())
            for character in self.content_dict[class_].keys():
                self.content_dict[class_][character] /= total_texts
            # print_counter(self.content_dict[class_], k=10, title=class_)

        '''
        Output dictionary result.
        '''
        for class_ in classes:
            self.content_dict[class_] = dict(self.content_dict[class_])
        self.content_dict['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.txt_root+'classify.dictionary', 'w') as f:
            f.write(json.dumps(self.content_dict))

        print('Creating words dictionary finished!')

    def test_texts(self):
        with open(self.dictionary_path) as f:
            self.content_dict = json.loads(f.read())
        print('Using dictionary generated at %s.' % self.content_dict['time'])

        test_dict = {}
        for class_ in classes:
            file_list = os.listdir(self.img_root+class_+'/')
            choose = [x[:-3]+'txt' for x in choices(file_list, k=7)]
            for item in choose:
                if item in os.listdir(self.txt_root+'txt/'):
                    test_dict[item] = class_

        for txt_file in test_dict.keys():
            print('----- Evaluating [%s], should be [%s] -----' % (txt_file[:-4], test_dict[txt_file]))
            self.test_master(txt_file, mode='already_read')

    def test_master(self, fn, mode='print', dir_prefix=''):

        if mode != 'already_read':
            with open(dir_prefix+self.dictionary_path) as f:
                self.content_dict = json.loads(f.read())
            print('Using dictionary generated at %s.' % self.content_dict['time'])

        with open(self.txt_root + 'txt/' + fn) as f:
            content = f.read()
        result_list = []
        for class_ in classes:
            eval_score = 0
            fail_num = 0
            chara_num = len(content)
            for character in list(content):
                try:
                    eval_score += self.content_dict[class_][character]
                except KeyError:
                    fail_num += 1
            if mode == 'print':
                print('\t%s = [%.6f]' % (class_, eval_score / (chara_num - fail_num) * TIMES))
            else:
                try:
                    result_list.append((class_, eval_score / (chara_num - fail_num) * TIMES))
                except ZeroDivisionError:
                    print('[ x ] FATAL: Cannot find any text in %s!' % fn)
                    result_list.append((class_, 0.))
        return result_list


TIMES = 150

if __name__ == '__main__':

    t = TextClassifier()
    # t.create_dict()
    t.test_texts()
