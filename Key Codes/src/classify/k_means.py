import sqlite3
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy


def title(t):
    print('\n------------------------ %s ------------------------' % t)


conn = sqlite3.connect('../../db/classification.db')
c = conn.cursor()

# c.execute("SELECT * FROM result WHERE usage='train'")
c.execute("SELECT * FROM result")
all_records = c.fetchall()

# data = [record[3:] for record in all_records]

data = []
report_num = 0
for record in all_records:
    if record[1] == 'report':
        report_num += 1
    data.append(list(record[3:])+[record[6]-record[7]])  # +[0.0 if record[6] == 0 else record[5]/record[6]]

max_iter = 100
print('\n\n[PARAMS] Max_iter = %d' % max_iter)

clf = KMeans(
    n_clusters=2,
    max_iter=max_iter
)
s = clf.fit(data)

test_1 = clf.labels_[24:136]
test_2 = clf.labels_[136:235]
test_3 = clf.labels_[235:376]
counts_1 = numpy.bincount(test_1)
counts_2 = numpy.bincount(test_2)
counts_3 = numpy.bincount(test_3)

labels = {
    'report': numpy.argmax(counts_3),
    'paper_n_report': numpy.argmax(counts_2),
    'n_paper': numpy.argmax(counts_1)
}

real_label = numpy.array([labels[x[1]] for x in all_records])

# title('Real labels')
# print(real_label.__str__())
# title('Cluster labels')
# print(clf.labels_)

title('Diff labels')
print(' ', end='')
diff_num = 0
for index, r in enumerate(clf.labels_):
    if real_label[index] != r:
        print('\033[1;31m%d\033[0m' % r, end=' ')
        if real_label[index] == labels['report']:
            diff_num += 1
    else:
        print(r, end=' ')
    if index % 37 == 36:
        print('\n', end=' ')

correction = 100 - diff_num/report_num*100
print('\n\n[SUMMARY] Predict correction = %.1f%%.\n' % correction)

for i in range(len(real_label)):
    if real_label[i] == labels['report']:
        if real_label[i] != clf.labels_[i]:
            print('[ x ] %8s %8s %0s %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f' % tuple(all_records[i]))
        # else:
        #     print('[ √ ] %8s %8s %0s %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f' % tuple(all_records[i]))

joblib.dump(clf, '../models/k_means_0879.pkl')
