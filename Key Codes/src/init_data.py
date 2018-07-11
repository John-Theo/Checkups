import sqlite3
import numpy as np
from sklearn.utils import Bunch


def load_checkup():
    standardize_dict = {
        'report': 0,
        'paper_n_report': 1,
        'n_paper': 1
    }

    conn = sqlite3.connect('../../db/classification.db')
    c = conn.cursor()
    c.execute("SELECT * FROM result")
    all_records = c.fetchall()
    conn.close()

    data_list = []
    target_list = []

    for record in all_records:
        data_list.append(
            list(record[3:])
        )
        target_list.append(standardize_dict[record[1]])

    data_set = Bunch()

    data_set.data = np.array(data_list)
    data_set.target = np.array(target_list)

    data_set.feature_names = [
        'IMG_report',
        'IMG_paper_n_report',
        'IMG_n_paper',
        'TXT_report',
        'TXT_paper_n_report',
        'TXT_n_paper'
    ]
    data_set.target_names = [
        'report',
        'paper_n_report | n_paper'
    ]
    return data_set
