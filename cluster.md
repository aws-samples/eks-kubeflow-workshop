This guidance shows how to run an AWS EKS cluster for kubeflow workshop.

## EKS Optimized AMI image with GPU support
The Amazon EKS-optimized AMI with GPU support is built on top of the standard Amazon EKS-optimized AMI, and is configured to serve as an optional image for Amazon EKS worker nodes to support GPU workloads.

Please subscribe it in [AWS Marketplace](https://aws.amazon.com/marketplace/pp/B07GRHFXGM).

## eksctl config
In this workshop, we highly recommend you to create an EKS cluster using eksctl CLI tool. While, you can also create AWS EKS cluster, using AWS EKS CLI, CloudFormation or Terraform, AWS CDK.

It is possible to pass all parameters to the tool as CLI flags or configuration file. Using configuration file makes process more repeatable and automation friendly.

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: kfworkshop
  region: us-west-2
  version: '1.13'
# If your region has multiple availability zones, you can specify 3 of them.
#availabilityZones: ["us-west-2b", "us-west-2c", "us-west-2d"]

# NodeGroup holds all configuration attributes that are specific to a nodegroup
# You can have several node group in your cluster.
nodeGroups:
  - name: cpu-nodegroup
    instanceType: m5.xlarge
    desiredCapacity: 2
    minSize: 0
    maxSize: 4
    volumeSize: 30
    ssh:
      allow: true
      publicKeyPath: '~/.ssh/id_rsa.pub'

  # Example of GPU node group
  - name: Tesla-V100
    instanceType: p3.8xlarge
    availabilityZones: ["us-west-2b"]
    desiredCapacity: 0
    minSize: 0
    maxSize: 4
    volumeSize: 50
    ssh:
      allow: true
      publicKeyPath: '~/.ssh/id_rsa.pub'
```
> Note: we create one CPU and one GPU node groups. GPU desired capacity is set to 0 and you can scale up GPU node groups to use acceslarator nodes.
> Most of the experiements will use CPU here can be done with CPU.

### Create EKS Cluster

Run this command to create EKS cluster

```
eksctl create cluster -f cluster.yaml
```