## Kubeflow Labs on EKS

### Use Fairing Kaniko Cloud Builder with Kubeflow on AWS
I build ecr container image by using Fairing Kaniko, and then utilize the image for training job.

### Use container image with awscli, docker client

I build a container image with awscli and docker support, Please use `seedjeffwan/tensorflow-1.13.1-notebook-cpu:awscli-v2` as a custom image to provision your notebook. I am working on upstream patch it will be ready soon.


### ECR permission

Since fairing library will create ECR repository, upload repository to ECR, and put objects in S3 bucket. Grant `AmazonEC2ContainerRegistryFullAccess` and `AmazonS3FullAccess` to your node group role.  (We will use simplest policies instead later)

### Disable istio inject for your namespace(Optional)
In order to succesfully run fairing, you need to label your namespace. `anonymous` is the namespace we want to use, change to your namespace if you use a different one

```
 kubectl edit ns anonymous
```

Be default, istio inject is enabled at the namespace level. Add `istio-injection: disabled` to avoid istio inject sidecar pods.

```
  labels:
    istio-injection: disabled
```

Check [Disable istio-injection in namespace profile controller creates?](https://github.com/kubeflow/kubeflow/issues/3935) for details
