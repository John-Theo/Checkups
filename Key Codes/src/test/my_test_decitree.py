from sklearn.externals import joblib
import sqlite3
import random

clf = joblib.load('../models/decision_tree_0981.pkl')

conn = sqlite3.connect('../../db/classification.db')
c = conn.cursor()
c.execute("SELECT * FROM result")
# c.execute("SELECT * FROM result")
all_records = random.sample(c.fetchall(), 100)
if all_records is []:
    print('[FATAL] No record retrieved!')
conn.close()

TP = 0
TN = 0
FP = 0
FN = 0

for record in all_records:
    predict = clf.predict([list(record[3:])])
    if record[1] == 'report':
        if predict == 0:
            TP += 1
        else:
            FP += 1
    else:
        if predict == 1:
            TN += 1
        else:
            FN += 1

if TP < FP:
    TP, FP = FP, TP
if TN < FN:
    TN, FN = FN, TN

try:
    print('Number of TP: %d;  Number of FP: %d;  Accuracy = [%.1f%%]' % (TP, FP, TP/(TP+FP)*100))
    print('Number of TN: %d;  Number of FN: %d;  Accuracy = [%.1f%%]' % (TN, FN, TN/(TN+FN)*100))
except ZeroDivisionError:
    pass
