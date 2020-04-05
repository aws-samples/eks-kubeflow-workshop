def tfj_spec(train_name, num_ps, num_workers, model_dir, export_path, train_steps, batch_size, learning_rate, image, AWS_REGION):
  train_spec = f"""apiVersion: kubeflow.org/v1
kind: TFJob
metadata:
  name: {train_name}  
spec:
  tfReplicaSpecs:
    Ps:
      replicas: {num_ps}
      template:
        metadata:
          annotations:
            sidecar.istio.io/inject: "false"
        spec:
          serviceAccount: default-editor
          containers:
          - name: tensorflow
            command:
            - python
            - /opt/model.py
            - --tf-model-dir={model_dir}
            - --tf-export-dir={export_path}
            - --tf-train-steps={train_steps}
            - --tf-batch-size={batch_size}
            - --tf-learning-rate={learning_rate}
            image: {image}
            workingDir: /opt
            env:
            - name: AWS_REGION
              value: {AWS_REGION}
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: AWS_ACCESS_KEY_ID
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: AWS_SECRET_ACCESS_KEY

          restartPolicy: OnFailure
    Chief:
      replicas: 1
      template:
        metadata:
          annotations:
            sidecar.istio.io/inject: "false"
        spec:
          serviceAccount: default-editor
          containers:
          - name: tensorflow
            command:
            - python
            - /opt/model.py
            - --tf-model-dir={model_dir}
            - --tf-export-dir={export_path}
            - --tf-train-steps={train_steps}
            - --tf-batch-size={batch_size}
            - --tf-learning-rate={learning_rate}
            image: {image}
            workingDir: /opt
            env:
            - name: AWS_REGION
              value: {AWS_REGION}
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: AWS_ACCESS_KEY_ID
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: AWS_SECRET_ACCESS_KEY

          restartPolicy: OnFailure
    Worker:
      replicas: 1
      template:
        metadata:
          annotations:
            sidecar.istio.io/inject: "false"
        spec:
          serviceAccount: default-editor
          containers:
          - name: tensorflow
            command:
            - python
            - /opt/model.py
            - --tf-model-dir={model_dir}
            - --tf-export-dir={export_path}
            - --tf-train-steps={train_steps}
            - --tf-batch-size={batch_size}
            - --tf-learning-rate={learning_rate}
            image: {image}
            workingDir: /opt
            env:
            - name: AWS_REGION
              value: {AWS_REGION}
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: AWS_ACCESS_KEY_ID
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: AWS_SECRET_ACCESS_KEY
          restartPolicy: OnFailure
"""

  return train_spec