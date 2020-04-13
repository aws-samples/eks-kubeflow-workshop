import logging
import json
import pandas as pd
import numpy as np
import argparse
import ssl

from sklearn import model_selection
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from tensorflow.python.lib.io import file_io


def create_parser():
    parser = argparse.ArgumentParser(description='IRIS Pipeline Metrics Visualization Example')

    parser.add_argument('--input_url', type=str.strip, required=False, help='The Input dataset url',
                        default='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
    parser.add_argument('--input_column_names', type=list, required=False, help='The Input dataset column names',
                        default=['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'species'])
    parser.add_argument('--test_size', type=float, required=False,
                        help='The test dataset portion among the raw dataset', default=0.2)
    parser.add_argument('--train_random_seed', type=int, required=False, help='The training random seed', default=7)

    return parser


def preprocess(args):
    iris = pd.read_csv(args.input_url, names=args.input_column_names)
    array = iris.values
    X, y = array[:, 0:4], np.where(array[:, 4] == 'Iris-setosa', 1, 0)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=args.test_size,
                                                                        random_state=args.train_random_seed)

    return X_train, X_test, y_train, y_test


def sklearn_training(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)

    return model


def inference(model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_pred, y_test)

    y_score = model.decision_function(X_test)
    auc = roc_auc_score(y_test, y_score)

    return acc, auc


def write_metadata(acc, auc):
    metrics = {
        'metrics': [{
            'name': 'accuracy-score',  # The name of the metric. Visualized as the column name in the runs table.
            'numberValue': acc,  # The value of the metric. Must be a numeric value.
            'format': "PERCENTAGE",  # The optional format of the metric.
        },
        {
            'name': 'roc-auc-score',
            'numberValue': auc,
            'format': "PERCENTAGE"
        }]
    }

    with file_io.FileIO('/mlpipeline-metrics.json', 'w') as f:
        json.dump(metrics, f)

    logging.info("Succeed in Writing Metrics")


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    # Bypass ssl verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Preprocess
    X_train, X_test, y_train, y_test = preprocess(args)

    # Sklearn Training
    sk_model = sklearn_training(X_train, y_train)

    # Inference
    acc, auc = inference(sk_model, X_test, y_test)

    # write into metadata json
    write_metadata(acc, auc)


if __name__ == "__main__":
    main()
