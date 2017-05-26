# coding: utf-8
import warnings
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import IncrementalPCA

from sklearn import metrics


def clean_df(df):
    new_df = df.drop_duplicates(subset=['meta_name', 'x_coords', 'y_coords', 'block_height', 'block_width'])
    new_df = new_df[new_df['tag'] != 'meta']
    new_df = new_df[new_df['x_coords'] != 0]
    new_df = new_df[new_df['block_height'] != 0]
    new_df = new_df[new_df['block_width'] != 0]
    new_df.url = new_df.url.apply(lambda x: x.replace('\n', ''))
    return new_df


def get_domain(url):
    parts = url.split('//', 1)
    return parts[1].split('/', 1)[0].replace('www.', '')


def get_X(field, no_field, no_column_name):
    # balance the dataset

    no_field_smpl = no_field.sample(n=field.shape[0], random_state=7)
    real_train_meta_name = no_field_smpl.meta_name

    no_field_smpl = no_field_smpl.drop('meta_name', 1)
    no_field_smpl.insert(1, 'meta_name', no_column_name)

    X_field = pd.concat((field, no_field_smpl), axis=0)

    return X_field, real_train_meta_name


def fair_train_test_split(data):
    le_y = LabelEncoder()
    y_encoded = le_y.fit_transform(data.meta_name.values)
    data.meta_name = y_encoded

    data_one_domain = data[data.domain_mark == 1]
    data_other_domain = data[data.domain_mark != 1]

    y_one_domain = data_one_domain.meta_name
    y_other_domain = data_other_domain.meta_name

    data_one_domain = data_one_domain.drop(['meta_name', 'domain_mark'], 1)
    data_other_domain = data_other_domain.drop(['meta_name', 'domain_mark'], 1)

    X_train1, X_test1, y_train1, y_test1 = train_test_split(data_one_domain, y_one_domain, test_size=0.20)
    X_train2, X_test2, y_train2, y_test2 = train_test_split(data_other_domain, y_other_domain, test_size=0.80)
    return X_train1, X_test2, y_train1, y_test2


def get_splits_component(field_name, data):
    # Devide the set on positiva and negative examples    
    df_pos = data[data['meta_name'] == field_name]
    df_neg = data[data['meta_name'] != field_name]

    # Make the sample stratified by classes
    num_pos = df_pos.shape[0]
    df_neg_smpl = df_neg.sample(num_pos)

    no_column_name = 'no_' + field_name
    X, real_train_meta_name = get_X(df_pos, df_neg_smpl, no_column_name)

    # Randomly separate into train and test such that domains are not intersected
    X_rand_domain = assign_rand_domain_mark(X)
    X_train, X_test, y_train, y_test = fair_train_test_split(X_rand_domain)

    X_test = X_test.drop('domain', 1)
    X_train = X_train.drop('domain', 1)

    X_train_scale = StandardScaler().fit_transform(X_train)
    X_test_scale = StandardScaler().fit_transform(X_test)

    X_train = pd.DataFrame(X_train_scale, columns=X_train.columns)
    X_test = pd.DataFrame(X_test_scale, columns=X_test.columns)

    return X_train, X_test, y_train, y_test


def assign_rand_domain_mark(data):
    # half of the domains will marked 1, half 0

    domains = data.domain.unique()
    smpl_num = int(len(domains) * 0.5)
    yes = np.random.choice(domains, smpl_num)
    data['domain_mark'] = 1
    data.ix[~data.domain.isin(yes), 'domain_mark'] = 0
    return data


def draw_feature_importance(clf_forest, X_train, field_name):
    importances = clf_forest.feature_importances_
    #     std = np.std([tree.feature_importances_ for tree in clf_forest.estimators_],
    #                  axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X_train.shape[1]):
        print("%d. feature '%s' (%f)" % (indices[f], X_train.columns[indices[f]], importances[indices[f]]))

    indices_text = [X_train.columns[indices[f]] for f in range(X_train.shape[1])]
    # Plot the feature importances of the forest
    plt.figure(figsize=(10, 8))
    plt.title("Feature importances for {}".format(field_name))
    plt.bar(range(X_train.shape[1]), importances[indices],
            color="g", align="center")  # ,yerr=std[indices]
    plt.xticks(range(X_train.shape[1]), indices_text)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=70)
    plt.xlim([-1, X_train.shape[1]])

    plt.show()


def get_clf_by_name(estimator_name, param_grid):
    if estimator_name == "Random Forest":
        clf = RandomForestClassifier(n_estimators=1000)
    elif estimator_name == "Extreme Random Forest":
        clf = ExtraTreesClassifier(n_estimators=500)
    elif estimator_name == "SVM":
        clf = SVC()
    elif estimator_name == "Logistic regression":
        clf = LogisticRegression()

    if param_grid:
        return GridSearchCV(estimator=clf, param_grid=param_grid)
    else:
        return clf


def append_pca_tfidf_and_scale(X_train, X_test):
    # PCA estimator
    # Inputs are already standartized
    # Removes text field in the end

    # tf-idf estimator
    tfidf_train_vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.7)
    tfidf_test_vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.7)

    # fit_transform text string to tf-idf matrix
    tfidf_train = tfidf_train_vectorizer.fit_transform(X_train.text).todense()
    tfidf_test = tfidf_test_vectorizer.fit_transform(X_test.text).todense()

    # PCA estimators
    pca_train_tfidf = IncrementalPCA(n_components=5, batch_size=5).fit_transform(tfidf_train)
    pca_test_tfidf = IncrementalPCA(n_components=5, batch_size=5).fit_transform(tfidf_test)

    # drop text column and append pca
    X_train = X_train.drop('text', 1)
    X_test = X_test.drop('text', 1)

    pca_train = pd.DataFrame(pca_train_tfidf, index=X_train.index)
    pca_test = pd.DataFrame(pca_test_tfidf, index=X_test.index)

    X_train_new = pd.concat([X_train, pca_train], axis=1)
    X_test_new = pd.concat([X_test, pca_test], axis=1)

    X_train_scale = StandardScaler().fit_transform(X_train_new)
    X_test_scale = StandardScaler().fit_transform(X_test_new)

    columns_train = X_train.columns.tolist() + pca_train.columns.tolist()
    columns_test = X_test.columns.tolist() + pca_test.columns.tolist()

    X_train = pd.DataFrame(X_train_scale, columns=columns_train)
    X_test = pd.DataFrame(X_test_scale, columns=columns_test)

    return X_train, X_test


def analyse(field_name, data, estimator_name, **kwargs):
    """
    Cross validation k = 5
    Domains don't intersect
    Option to optimize params - send 'param_grid' Dict()
    May include PCA of tf-idf matrix - send 'tf_idf' boolean
    Draw feature importance for forests

    :param field_name: event component name
    :param data: dataset with 'meta_name', 'text', 'domain' and numeric features, no NA
    :param kwargs: 'param_grid' - Dict(), 'tf_idf' - boolean
    :return: tables with metrics: accuracy, precision, recall, f1
    """

    param_grid = kwargs.get('param_grid')
    is_opt = param_grid is not None
    print("Current model: {}, Prameter optimization: {}".format(estimator_name, is_opt))

    mean_accuracy = []
    f1_score = []
    precision = []
    recall = []

    num_iter = 1 if is_opt else 5

    clf = None
    X_train = None

    for i in range(num_iter):
        print("{}/{} iteration ...".format(i + 1, num_iter))
        clf = get_clf_by_name(estimator_name, param_grid)

        X_train, X_test, y_train, y_test = get_splits_component(field_name, data)

        if kwargs.get('tf_idf'):
            print("tf-idf and PCA: True")
            X_train, X_test = append_pca_tfidf_and_scale(X_train, X_test)

        if is_opt:
            clf = clf.best_estimator_
            print("Best params for {}:\n{}".format(estimator_name, clf.best_params_))

        clf.fit(X_train, y_train)
        test_score = clf.score(X_test, y_test)

        y_test_pred = clf.predict(X_test)

        f1_score.append(metrics.f1_score(y_pred=y_test_pred, y_true=y_test))
        precision.append(metrics.precision_score(y_pred=y_test_pred, y_true=y_test))
        recall.append(metrics.recall_score(y_pred=y_test_pred, y_true=y_test))
        mean_accuracy.append(test_score)

        print("Mean accuracy {0:.4f}".format(test_score))

    print("The final CV=5 score for {} and {}: ".format(field_name, estimator_name) + "{0:.4f}".format(
        np.mean(mean_accuracy)))

    result = pd.DataFrame({"mean_accuracy": [np.mean(mean_accuracy)],
                           "f1_score": [np.mean(f1_score)],
                           "precision": [np.mean(precision)],
                           "recall": [np.mean(recall)]
                           })
    print("METRICS:")
    print(result)
    print("Feature importance:")

    if "Forest" in estimator_name:
        # pick the last classifier to draw feature importance
        draw_feature_importance(clf, X_train, field_name)

    return result