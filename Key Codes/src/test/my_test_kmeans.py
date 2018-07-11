from sklearn.externals import joblib
import sqlite3

clf = joblib.load('../models/k_means_0970.pkl')

conn = sqlite3.connect('../../db/classification.db')
c = conn.cursor()
c.execute("SELECT * FROM result WHERE usage='test'")
# c.execute("SELECT * FROM result")
all_records = c.fetchall()
if all_records is []:
    print('[FATAL] No record retrieved!')
conn.close()

TP = 0
TN = 0
FP = 0
FN = 0

for record in all_records:
    predict = clf.predict([list(record[3:]) + [record[6] - record[7]]])
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
    print(TP, FP, TP/(TP+FP))
    print(TN, FN, TN/(TN+FN))
except ZeroDivisionError:
    pass
