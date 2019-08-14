## Kubeflow Workshop on EKS

This repo is a Kubeflow Workshop on EKS and it will covers most of the cutting edge components in Kubeflow. The Lab is designed for native AWS and it will leverage a few AWS services like ECR, S3, EFS, FSX for Lustre, Cognito, Certificate Manager, etc.


## Prerequisites

* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl)
* Install and configure the AWS Command Line Interface (AWS CLI):
    * Install the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).
    * Configure the AWS CLI by running the following command: `aws configure`.
    * Enter your Access Keys ([Access Key ID and Secret Access Key](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)).
    * Enter your preferred AWS Region and default output options.
* Install [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html).
* Install [eksctl](https://github.com/weaveworks/eksctl) (version 0.1.31 or newer)


## Setups

1. [Create an EKS cluster](cluster.md) or bring your own EKS cluster.
2. [Setup up Kubeflow](kubeflow.md)
3. [Post Installation](post-install.md)

## Labs
- [Model Development in Jupyter Notebook](notebooks/01_Jupyter_Notebook)
- [Fairing](notebooks/02_Fairing)
- [Distributed Training](notebooks/03_Distributed_Training)
- [Tensorflow Extended](notebooks/04_Tensorflow_Extended)
- [Kubeflow Pipeline](notebooks/05_Kubeflow_Pipeline)
- Serving
- [Experiment Tracking](notebooks/07_Experiment_Tracking)
- [HyperParameter Tuning](notebooks/08_Hyperparameter_Tuning)
- Monitoring
- Logs


## Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your bug report or contribution.


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security issue notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](https://github.com/aws-samples/deep-learning-benchmark/blob/master/LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.

We may ask you to sign a [Contributor License Agreement (CLA)](http://en.wikipedia.org/wiki/Contributor_License_Agreement) for larger changes.

