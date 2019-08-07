
Build MLFLOW container image, # 1.0.0 is current mlflow version
```
docker build -t seedjeffwan/mlflow-tracking-server:1.0.0 .
```


Command to check MLFLOW UI locally
```
kubectl port-forward deployment/mlflow-tracking-server -n kubeflow 5000:5000
```
