### ALB ingress controller doesn't have hostname
See details here.
https://www.kubeflow.org/docs/aws/troubleshooting-aws/#alb-can-not-be-created


### 02_01_fairing_introduction.ipynb

```
Using preprocessor: <kubeflow.fairing.preprocessors.function.FunctionPreProcessor object at 0x7f465477d198>
Using builder: <kubeflow.fairing.builders.append.append.AppendBuilder object at 0x7f464c5a6470>
Using deployer: <kubeflow.fairing.builders.append.append.AppendBuilder object at 0x7f464c5a6470>
Building image using Append builder...
Creating docker context: /tmp/fairing_context_vxtx276v
/opt/conda/lib/python3.6/site-packages/kubeflow/fairing/__init__.py already exists in Fairing context, skipping...
Loading Docker credentials for repository 'tensorflow/tensorflow:1.14.0-py3'
Image successfully built in 0.9853512160007085s.
Pushing image <your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fairing-job:D095EFDD...
Loading Docker credentials for repository '<your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fairing-job:D095EFDD'
Uploading <your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fairing-job:D095EFDD
Error during upload of: <your_account_id>.dkr.ecr.us-west-2.amazonaws.com/fairing-job:D095EFDD
```

Grant `AmazonEC2ContainerRegistryFullAccess` to your node group role

```
V2DiagnosticException: response: {'content-type': 'application/json; charset=utf-8', 'date': 'Thu, 31 Oct 2019 21:54:33 GMT', 'docker-distribution-api-version': 'registry/2.0', 'content-length': '296', 'connection': 'keep-alive', 'status': '403'}
User: arn:aws:sts::<your_account_id>:assumed-role/eksctl-eksworkshop-nodegroup-eks-NodeInstanceRole-YSDP5QKKX4GX/i-09a280xxxxxx941b is not authorized to perform: ecr:InitiateLayerUpload on resource: arn:aws:ecr:us-west-2:<your_account_id>:repository/fairing-job: None
```

Same permission issue as above one.


```
V2DiagnosticException: response: {'content-type': 'application/json; charset=utf-8', 'date': 'Thu, 31 Oct 2019 22:05:59 GMT', 'docker-distribution-api-version': 'registry/2.0', 'content-length': '142', 'connection': 'keep-alive', 'status': '404'}
The repository with name 'fairing-job' does not exist in the registry with id '<your_account_id>': None

```

You need to create a `fairing-job` ECR repository there to host fairing jobs.

