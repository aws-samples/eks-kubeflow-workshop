This instructions show how to setup a EFS share between Kubeflow Jupyter notebook and SageMaker notebook.

## Setup EFS on an exisiting EKS cluster.

Please follow this step [here](https://www.kubeflow.org/docs/aws/storage/) to create an EFS mount.

When you setup your EFS filesystem, make sure that you use the same VPC from your EKS cluster and the same security group as the EKS ClusterSharedSecurityGroup.

## Create a SageMaker notebook.

When creating a SageMaker notebook, make sure that you select the same VPC and subnet (pick one and make note of the availability zone) as your EKS cluster.

In the EFS console, look up the IP address for the same subnet or availability zone. We will be using that IP address to create a mount point in SageMaker.

In SageMaker create a terminal.

Make sure that you are in the SageMaker folder and create a directory called data.

```
mkdir ./data
```

Enter the following command to create a mount point.

```
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 <EFS_IP_ADDRESS>:/ ./data
```

Change the permissions to the mount folder.
```
sudo chmod go+rw ./data
```

If you are looking for more information on how to mount an EFS file system on SageMaker, please look at the following [blogpost.](https://aws.amazon.com/blogs/machine-learning/mount-an-efs-file-system-to-an-amazon-sagemaker-notebook-with-lifecycle-configurations/)


