
# Background
Deep learning has shown that being able to train large models on vasts amount of data can drastically improve model performance. However, consider the problem of training a deep network with millions, or even billions of parameters. How do we achieve this without waiting for days, or even multiple weeks? Dean et al. [2] propose a different training paradigm which allows us to train and serve a model on multiple physical machines. The authors propose two novel methodologies to accomplish this, namely, model parallelism and data parallelism. In the following blog post, we briefly mention model parallelism since we will mainly focus on data parallel approaches.
https://joerihermans.com/ramblings/distributed-deep-learning-part-1-an-introduction/


# Data parallelism

# Model Parallelism

# Distributed Training in Tensorflow 
"Data Parallelism" is the most common training configuration, it involves multiple tasks in a `worker` job training the same model on different mini-batches of data, updating shared parameters hosted in one or more tasks in a `ps` (parameter server) job. All tasks typically run on different machines or containers. There are many ways to specify this structure in TensorFlow, and Tensorflow team are building libraries that will simplify the work of specifying a replicated model. 

- In-graph replication. In this approach, the client builds a single tf.Graph that contains one set of parameters (in tf.Variable nodes pinned to /job:ps); and multiple copies of the compute-intensive part of the model, each pinned to a different task in /job:worker.

- Between-graph replication. In this approach, there is a separate client for each /job:worker task, typically in the same process as the worker task. Each client builds a similar graph containing the parameters (pinned to /job:ps as before using tf.train.replica_device_setter to map them deterministically to the same tasks); and a single copy of the compute-intensive part of the model, pinned to the local task in /job:worker.

- Asynchronous training. In this approach, each replica of the graph has an independent training loop that executes without coordination. It is compatible with both forms of replication above.

- Synchronous training. In this approach, all of the replicas read the same values for the current parameters, compute gradients in parallel, and then apply them together. It is compatible with in-graph replication (e.g. using gradient averaging as in the CIFAR-10 multi-GPU trainer), and between-graph replication (e.g. using the tf.train.SyncReplicasOptimizer).
https://github.com/tensorflow/examples/blob/master/community/en/docs/deploy/distributed.md


# Ring Allreduce

The standard distributed TensorFlow package runs with a parameter server approach to averaging gradients. In this approach, each process has one of two potential roles: a worker or a parameter server. Workers process the training data, compute gradients, and send them to parameter servers to be averaged.

Challenges of Tensorflow distributed training

- Identifying the right ratio of worker to parameter servers: If one parameter server is used, it will likely become a networking or computational bottleneck. If multiple parameter servers are used, the communication pattern becomes “all-to-all” which may saturate network interconnects.

- Handling increased TensorFlow program complexity: 
During our testing, every user of distributed TensorFlow had to explicitly start each worker and parameter server, pass around service discovery information such as hosts and ports of all the workers and parameter servers, and modify the training program to construct tf.Server() with an appropriate tf.ClusterSpec(). Additionally, users had to ensure that all the operations were placed appropriately using tf.train.device_replica_setter() and code is modified to use towers to leverage multiple GPUs within the server. This often led to a steep learning curve and a significant amount of code restructuring, taking time away from the actual modeling.

- Bandwidth is not optimal, network could be the bottleneck: If model has more parameters, network traffic grow with number of parameters. This is not a scalable solution. 


# Horovod
In early 2017, Baidu published an article, “Bringing HPC Techniques to Deep Learning,” evangelizing a different algorithm for averaging gradients and communicating those gradients to all nodes. 

In the ring-allreduce algorithm, each of N nodes communicates with two of its peers 2*(N-1) times. During this communication, a node sends and receives chunks of the data buffer. In the first N-1 iterations, received values are added to the values in the node’s buffer. In the second N-1 iterations, received values replace the values held in the node’s buffer. Baidu’s paper suggests that this algorithm is bandwidth-optimal, meaning that if the buffer is large enough, it will optimally utilize the available network.


# MPI
Users utilize a Message Passing Interface (MPI) implementation such as Open MPI to launch all copies of the TensorFlow program. MPI then transparently sets up the distributed infrastructure necessary for workers to communicate with each other.  All the user needs to do is modify their program to average gradients using an allreduce() operation.

# Horovod

The realization that a ring-allreduce approach can improve both usability and performance motivated us to work on our own implementation to address Uber’s TensorFlow needs. Uber adopted Baidu’s draft implementation of the TensorFlow ring-allreduce algorithm and built upon it. That's horovod.


```
kubectl apply -f tensorflow.yaml
```



```
kubectl apply -f mpijob.yaml

```