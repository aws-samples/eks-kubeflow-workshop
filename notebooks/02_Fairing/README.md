## Kubeflow Labs on EKS

### Use Fairing Kaniko Cloud Builder with Kubeflow on AWS
I build ecr container image by using Fairing Kaniko, and then utilize the image for training job.

### Use container image with awscli, docker client

I build a container image with awscli and docker support, Please use `seedjeffwan/tensorflow-1.13.1-notebook-cpu:awscli-v2` as a custom image to provision your notebook. I am working on upstream patch it will be ready soon.


### ECR permission

Since fairing library will create ECR repository, upload repository to ECR, and put objects in S3 bucket. Grant `AmazonEC2ContainerRegistryFullAccess` and `AmazonS3FullAccess` to your node group role.  (We will use simplest policies instead later)

We also provide an option to enable IAM Roles for Service Account. If you configure kubeflow from [option 1](https://www.kubeflow.org/docs/aws/deploy/install-kubeflow/#option-1-use-iam-for-service-account), then you can attach IAM Role `kf-user-${cluster_name}` with below policies which enables ECR and S3 operation.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*",
                "cloudtrail:LookupEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}
```