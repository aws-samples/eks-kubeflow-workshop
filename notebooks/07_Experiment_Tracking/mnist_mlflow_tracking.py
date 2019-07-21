from __future__ import print_function

import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import os
import subprocess
import argparse
import time

import mlflow
import mlflow.keras


# Reduce spam logs from s3 client
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

def preprocessing():
  fashion_mnist = keras.datasets.fashion_mnist
  (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

  # scale the values to 0.0 to 1.0
  train_images = train_images / 255.0
  test_images = test_images / 255.0

  # reshape for feeding into the model
  train_images = train_images.reshape(train_images.shape[0], 28, 28, 1)
  test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

  class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

  print('\ntrain_images.shape: {}, of {}'.format(train_images.shape, train_images.dtype))
  print('test_images.shape: {}, of {}'.format(test_images.shape, test_images.dtype))

  return train_images, train_labels, test_images, test_labels

def train(train_images, train_labels, epochs, model_summary_path):
  if model_summary_path:
    logdir=model_summary_path # + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

  model = keras.Sequential([
    keras.layers.Conv2D(input_shape=(28,28,1), filters=8, kernel_size=3,
                        strides=2, activation='relu', name='Conv1'),
    keras.layers.Flatten(),
    keras.layers.Dense(10, activation=tf.nn.softmax, name='Softmax')
  ])
  model.summary()

  model.compile(optimizer=tf.train.AdamOptimizer(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
                )
  if model_summary_path:
    model.fit(train_images, train_labels, epochs=epochs, batch_size=64, callbacks=[tensorboard_callback])
  else:
    model.fit(train_images, train_labels, epochs=epochs, batch_size=64)

  mlflow.log_param('batch_size', 64)

  return model

def eval(model, test_images, test_labels):
  test_loss, test_acc = model.evaluate(test_images, test_labels)
  print('\nTest accuracy: {}, test loss {}'.format(test_acc, test_loss))
  mlflow.log_metric("accuracy", test_acc)
  mlflow.log_metric("loss", test_loss)

def export_model(model, model_export_path):
  version = 1
  export_path = os.path.join(model_export_path, str(version))

  tf.saved_model.simple_save(
    keras.backend.get_session(),
    export_path,
    inputs={'input_image': model.input},
    outputs={t.name:t for t in model.outputs})

  print('\nSaved model: {}'.format(export_path))


def main(argv=None):
  parser = argparse.ArgumentParser(description='Fashion MNIST Tensorflow Example')
  parser.add_argument('--model_export_path', type=str, help='Model export path')
  parser.add_argument('--model_summary_path', type=str,  help='Model summry files for Tensorboard visualization')
  parser.add_argument('--epochs', type=int, default=5, help='Training epochs')
  args = parser.parse_args()

  # File Based Tracking URI. Use NFS in this case
  # users_home = '/tmp/shjiaxin'
  # experiment_base_path = '%s/experiments' % users_home
  # tracking_uri='file://%s' % experiment_base_path

  # Remote Tracking Server URI. Use kubernetes Service.
  tracking_uri = "http://mlflow-tracking-server:5000"
  mlflow.set_tracking_uri(tracking_uri)

  experiment_name = 'mlflow'
  mlflow.set_experiment(experiment_name)

  with mlflow.start_run() as run:
    start_time = time.time()
    train_images, train_labels, test_images, test_labels = preprocessing()
    model = train(train_images, train_labels, args.epochs, args.model_summary_path)
    eval(model, test_images, test_labels)

    mlflow.log_param('epochs', args.epochs)

    if args.model_export_path:
      export_model(model, args.model_export_path)

    # Use MLFlow fashion to persist model
    mlflow.keras.log_model(model, 'model_keras')

    # Measure running time
    duration_in_seconds = time.time() - start_time
    print("This model took", duration_in_seconds, "seconds to train and test.")
    mlflow.log_metric("time_duration", duration_in_seconds)

if __name__ == "__main__":
  main()
