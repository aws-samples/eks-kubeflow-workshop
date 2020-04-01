import logging
import json
import pandas as pd
import numpy as np
import os
import boto3
import tensorflow as tf
import datetime
import argparse

from sklearn import model_selection
from sklearn.metrics import confusion_matrix, roc_curve
from sklearn.linear_model import LogisticRegression
from tensorflow.python.lib.io import file_io
from botocore.exceptions import ClientError


def create_parser():
    parser = argparse.ArgumentParser(description='IRIS E2E Example')

    parser.add_argument('--aws_region', type=str.strip, required=False, help='The region of AWS Account',
                        default='us-west-2')
    parser.add_argument('--s3_bucket', type=str.strip, required=True, help='The S3 bucket name', default='')
    parser.add_argument('--s3_file_path_prefix', type=str.strip, required=False, help='The prefix of S3 file path',
                        default='iris-example')
    parser.add_argument('--input_url', type=str.strip, required=False, help='The Input dataset url',
                        default='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
    parser.add_argument('--input_column_names', type=list, required=False, help='The Input dataset column names',
                        default=['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'species'])
    parser.add_argument('--test_size', type=float, required=False,
                        help='The test dataset portion among the raw dataset', default=0.2)
    parser.add_argument('--train_random_seed', type=int, required=False, help='The training random seed', default=7)
    parser.add_argument('--tf_nn_optimizer', type=str.strip, required=False, help='Tensorflow neural network optimizer',
                        default='sgd')
    parser.add_argument('--tf_nn_loss_func', type=str.strip, required=False,
                        help='Tensorflow neural network loss function', default='sparse_categorical_crossentropy')
    parser.add_argument('--tf_nn_metrics', type=str.strip, required=False, help='Tensorflow neural network metrics',
                        default='accuracy')
    parser.add_argument('--tf_nn_epoch', type=int, required=False, help='Tensorflow neural network training epochs',
                        default=10)
    parser.add_argument('--tf_log_prefix', type=str.strip, required=False, help='The prefix of Tensorflow log file path',
                        default='/log/fit')

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
    md_text = "Trained Model's evaluation score: {}".format(model.score(X_test, y_test))
    md_file = os.path.join('/', 'train.md')
    with file_io.FileIO(md_file, 'w') as f:
        f.write(md_text)

    y_pred = model.predict(X_test)
    df = pd.concat([pd.DataFrame(y_test, columns=['target']), pd.DataFrame(y_pred, columns=['predicted'])], axis=1)
    vocab = list(df['target'].unique())
    cm = confusion_matrix(df['target'], df['predicted'], labels=vocab)
    data = []
    for target_index, target_row in enumerate(cm):
        for predicted_index, count in enumerate(target_row):
            data.append((vocab[target_index], vocab[predicted_index], count))
    df_cm = pd.DataFrame(data, columns=['target', 'predicted', 'count'])
    cm_file = os.path.join('/', 'confusion_matrix.csv')
    with file_io.FileIO(cm_file, 'w') as f:
        df_cm.to_csv(f, columns=['target', 'predicted', 'count'], header=False, index=False)

    y_score = model.decision_function(X_test)
    # Compute ROC curve and ROC area for each class
    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds})
    roc_file = os.path.join('/', 'roc.csv')
    with file_io.FileIO(roc_file, 'w') as f:
        df_roc.to_csv(f, columns=['fpr', 'tpr', 'thresholds'], header=False, index=False)

    return md_file, cm_file, roc_file, vocab


def tf_training(args, X_train, y_train, X_test, y_test):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),  # input shape required
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(2)
    ])

    model.compile(optimizer=args.tf_nn_optimizer,
                  loss=args.tf_nn_loss_func,
                  metrics=[args.tf_nn_metrics])

    time_hash = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_prefix = args.tf_log_prefix
    log_dir = os.path.join(log_prefix, time_hash)
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    model.fit(x=X_train,
              y=y_train,
              epochs=args.tf_nn_epoch,
              validation_data=(X_test, y_test),
              callbacks=[tensorboard_callback])

    return model, log_dir, time_hash


def upload_s3(args, md_file, cm_file, roc_file, log_dir, time_hash):
    AWS_REGION = args.aws_region
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    bucket = args.s3_bucket
    s3_file_path_prefix = args.s3_file_path_prefix

    try:
        # upload md file to S3
        md_object_name = 'train.md'
        s3_md_file = os.path.join('s3://', bucket, s3_file_path_prefix, md_object_name)
        s3_md_object = os.path.join(s3_file_path_prefix, md_object_name)
        s3_client.upload_file(md_file, bucket, s3_md_object)

        # upload cm file to S3
        cm_object_name = 'confusion_matrix.csv'
        s3_cm_file = os.path.join('s3://', bucket, s3_file_path_prefix, cm_object_name)
        s3_cm_object = os.path.join(s3_file_path_prefix, cm_object_name)
        s3_client.upload_file(cm_file, bucket, s3_cm_object)

        roc_object_name = 'roc.csv'
        s3_roc_file = os.path.join('s3://', bucket, s3_file_path_prefix, roc_object_name)
        s3_roc_object = os.path.join(s3_file_path_prefix, roc_object_name)
        s3_client.upload_file(roc_file, bucket, s3_roc_object)

        # upload tb log dir to S3
        tb_object_name = 'tb-logs'
        s3_tb_file = os.path.join('s3://', bucket, s3_file_path_prefix, tb_object_name)
        for path, subdirs, files in os.walk(log_dir):
            path = path.replace("\\", "/")
            directory_name = path.replace(log_dir, "")
            for file in files:
                if directory_name and directory_name[0] == '/':
                    directory_name = directory_name[1:]
                s3_client.upload_file(os.path.join(path, file), bucket,
                                      os.path.join(s3_file_path_prefix, 'tb-logs', time_hash, directory_name, file))
    except ClientError as e:
        logging.info("ERROR IN S3 UPLOADING!!!!!!")
        logging.ERROR(e)

    logging.info("S3 bucket path is: s3://{}/iris-example".format(bucket))

    return s3_md_file, s3_cm_file, s3_roc_file, s3_tb_file


def write_metadata(s3_md_file, s3_cm_file, s3_roc_file, s3_tb_file, vocab):
    metadata = {
        'outputs': [
            {
                'source': s3_md_file,
                'type': 'markdown',
            },
            {
                'type': 'confusion_matrix',
                'format': 'csv',
                'schema': [
                    {'name': 'target', 'type': 'CATEGORY'},
                    {'name': 'predicted', 'type': 'CATEGORY'},
                    {'name': 'count', 'type': 'NUMBER'},
                ],
                'source': s3_cm_file,
                # Convert vocab to string because for boolean values we want "True|False" to match csv data.
                'labels': list(map(str, vocab)),
            },
            {
                'type': 'roc',
                'format': 'csv',
                'schema': [
                    {'name': 'fpr', 'type': 'NUMBER'},
                    {'name': 'tpr', 'type': 'NUMBER'},
                    {'name': 'thresholds', 'type': 'NUMBER'},
                ],
                'source': s3_roc_file
            },
            {
                'type': 'tensorboard',
                'source': s3_tb_file,
            }
        ]
    }

    with file_io.FileIO('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)

    logging.info("Succeed in Writing Artifacts")


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    # Preprocess
    X_train, X_test, y_train, y_test = preprocess(args)

    # Sklearn Training
    sk_model = sklearn_training(X_train, y_train)

    # Inference
    md_file, cm_file, roc_file, vocab = inference(sk_model, X_test, y_test)

    # TF Training
    model, log_dir, time_hash = tf_training(args, X_train, y_train, X_test, y_test)

    # upload to S3
    s3_md_file, s3_cm_file, s3_roc_file, s3_tb_file = upload_s3(args, md_file, cm_file, roc_file, log_dir, time_hash)

    # write into metadata json
    write_metadata(s3_md_file, s3_cm_file, s3_roc_file, s3_tb_file, vocab)


if __name__ == "__main__":
    main()
