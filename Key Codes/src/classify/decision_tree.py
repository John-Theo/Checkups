from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from src.init_data import load_checkup
import numpy as np
from sklearn.externals.six import StringIO
import pydotplus
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


def visualize():
    dot_data = StringIO()
    tree.export_graphviz(
        best_clf,
        out_file=dot_data,
        feature_names=checkup.feature_names,
        class_names=checkup.target_names,
        filled=True, rounded=True,
        impurity=False
    )
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png("checkup.png")
    graph.write_pdf("checkup.pdf")


checkup = load_checkup()

sum_train, sum_test = 0, 0
iter_num = 36
best_clf, best_precision = None, 0.

for _ in range(iter_num):
    X_train, X_test, y_train, y_test = train_test_split(checkup.data, checkup.target, test_size=0.25)
    clf = tree.DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    accu_train = np.sum(clf.predict(X_train) == y_train)/float(y_train.size)
    accu_test = np.sum(clf.predict(X_test) == y_test)/float(y_test.size)

    print('Training & test set accuracy = [%.3f, %.3f]' % (float(accu_train), float(accu_test)))
    sum_test += accu_test
    sum_train += accu_train
    if float(accu_test) > best_precision:
        best_precision = float(accu_test)
        best_clf = clf

print('------------------------------------------------------')
print('Average accuracy = [%.3f, %.3f]' % (float(sum_train)/iter_num, float(sum_test)/iter_num))

print('Saving models...')
joblib.dump(best_clf, '../models/decision_tree_0'+str(best_precision)[2:5]+'.pkl')

print('Visualizing decision tree...')
visualize()
