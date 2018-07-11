import src.classify_data_generator as module_cdg
from sklearn.externals import joblib
import os
import matplotlib.pyplot as plt


def show_illustration():
    plt.figure(figsize=(21, 9))

    for index, file in enumerate(list(file_dict.keys())[:36]):
        try:
            img = plt.imread(TEST_FOLDER+file)
            plt.subplot(4, 9, index + 1)
            plt.title(file_dict[file], fontsize=8)
            plt.xticks(fontsize=2)
            plt.yticks(fontsize=2)
            plt.imshow(img)  # , plt.axis('off')
        except ValueError:
            print(file)

    plt.tight_layout()
    plt.show()


# file_name = '2.jpg'
TEST_FOLDER = '../../img/test/'

img_clf, txt_clf = None, None
cdg = module_cdg.ClsDataGen(TEST_FOLDER)

file_dict = {}
for file_name in os.listdir(TEST_FOLDER):
    if os.path.isdir(TEST_FOLDER+file_name):
        continue
    try:
        cdg.img_size_regulizer(file_name)
        img_clf = module_cdg.TestResult(cdg.image_classifier(file_name, dir_prefix='../'))
        txt_clf = module_cdg.TestResult(cdg.text_classifier(file_name, dir_prefix='../'))
    except AttributeError:
        print('[ x ] FATAL: Picture not qualified!')
        exit(0)

    result_list = []
    for method in ['IMG', 'TXT']:
        for rec_class_ in ['report', 'paper_n_report', 'n_paper']:
            if method == 'IMG':
                result_list.append(round(img_clf.my_dict[rec_class_] - 0, 3))
            else:
                result_list.append(round(txt_clf.my_dict[rec_class_] - 0, 3))

    print('\n---- Final Prediction ----')
    clf = joblib.load('../models/decision_tree_0981.pkl')
    result = ('report' if clf.predict([result_list]) == [0] else 'paper_n_report | n_paper')
    print('\t===>', result)
    file_dict[file_name] = result

show_illustration()
