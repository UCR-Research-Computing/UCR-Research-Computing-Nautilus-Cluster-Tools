# UCR RC Nautilus Cluster Tools

Scripts and configuration files developed and maintained UCR Research Computing that enables easy interaction with the Pacific Research Platform's Nautilus Cluster for UCR Researchers. Helping to promote PRP efforts.# UCR RC Nautilus Research Nodes

For UCR Researchers to provision and access Nautilus Cluster Research Nodes. These are very powerful GPU-enabled virtual servers made available by the Pacific Research Platform with access made possible and facilitated by UCR Research Computing.

## Kubernetes

The `PRP` is a Kubernetes cluster and therefore requires the use of a Kubernetes interface.
The command line Kubernetes interface `kubectl` is what is used in this workflow.

### Install

To run these actions locally on your local laptop/workstation you will need to install `kubectl` with the following commands:.

You can install `kubectl` via `conda`:

```bash
conda create -n kube -c anaconda-platform kubectl
```

If you do not yet have `conda` installed, follow these [instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).


You can install `kubectl` manually:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
mv kubectl ~/bin/.
```

### Config

For `kubectl` to function, it requires your `config` file provdied by `PRP`.
In order to get the `PRP` Kubernetes `config` file, do the following:
  1. Visit [Nautilus Portal](https://nautilus.optiputer.net/)
  2. Click on `Login` in upper right coner.
  3. Login using CILogon credentials (UCR `netID`).
  4. Once authenticated, click on the `Get config` in the upper right conner.
  5. This takes a while to dynamically generate, just wait and eventually your browser will present you a download prompt.
  6. Place this file in your `~/.kube` directory.

Next set the namespace, or else you will have to append the `-n ucr-rc` flag to every Kubernetes command:

```bash
kubectl config set-context nautilus --namespace=ucr-rc
```

## Nautilus script

Run with out any arguments and this script will spawn a RC Nautilus Research Node and drop you into the shell. You can also run abritraty commands on pop up workstations and list any active workstations you might have running. Please see the help for the command below for details on what options you can and funtions you can do. You can spawn any container you find on docker hub or other repos sas well as the default UCR Research Computing Nautilus Research Node.

```bash
./nautilus -h
usage: nautilus [-h] [-p CPUS] [-m MEMORY] [-g GPUS] [-n NAME] [-a AVAIL]
                [-r RUNNING] [-i INTERACTIVE] [-c CONTAINER] [-d COMMAND]

optional arguments:
  -h, --help            show this help message and exit

required named arguments:
  -p CPUS, --cpus CPUS  How many CPUs requested.
  -m MEMORY, --memory MEMORY
                        Number of GB of memory requested.
  -g GPUS, --gpus GPUS  Number of GPUs requested.
  -n NAME, --name NAME  Name for your workstation.
  -a AVAIL, --avail AVAIL
                        List common avaiable containers.
  -r RUNNING, --running RUNNING
                        List running workstations.
  -i INTERACTIVE, --interactive INTERACTIVE
                        To enter interactive mode.
  -c CONTAINER, --container CONTAINER
                        Name of container from DockerHub or PRP GitLab.
  -d COMMAND, --command COMMAND
                        Command to run on the workstation if not a shell.
```

### Launch node using the nautilus script.

```bash
./nautilus
Launching forsythc-research-lab-8159 Workstation Node ...
(base) jovyan@forsythc-research-lab-8159--1-jtvlx:~$
```
This drops you into the shell and you can install and use the node how ever you like.

### You can spawn any container you find on docker hub and other repos

```bash
./nautilus -c ubuntu:latest
./nautilus -c centos:latest
./nautilus -c rockylinux/rockylinux:latest
./nautilus -c gitlab-registry.nrp-nautilus.io/ucr-research-computing/ucr-rc-nautilus-genomics-conda-node:latest
```

### You can run arbitrary command on any container

```bash
./nautilus -c ubuntu:latest -d "uptime"
./nautilus -c centos:latest -d "cd /sharedvol ; wget https://ftp.ncbi.nlm.nih.gov/10GB ; ls"
./nautilus -c rockylinux/rockylinux:latest -d "hostname"
./nautilus -c gitlab-registry.nrp-nautilus.io/ucr-research-computing/ucr-rc-nautilus-genomics-conda-node:latest -d "conda install pandas"
```

### Reconnecting to a node or deleteing a node

When you exit the script it will ask if you want to save it for later use.

```bash
./nautilus
Launching forsythc-research-lab-8159 Workstation Node ...

(base) jovyan@forsythc-research-lab-8159--1-jtvlx:~$ exit
Enter 'y' to keep the forsythc-research-lab-8159 workstation node running for later?y
ok

```

```bash
Reconnect to the node
-- 'kubectl exec -it ucr-rc-nautilus-research-node-forsythc--1-njq66 -- bash'

Copy smaller files to the node
-- 'kubectl cp LOCALFILES ucr-rc-nautilus-research-node-forsythc--1-njq66:.'

Copy smaller files from the node
-- 'kubectl cp ucr-rc-nautilus-research-node-forsythc--1-njq66:REMOTEFILES LOCALFILES'

Delete the node
-- 'kubectl delete job ucr-rc-nautilus-research-node-forsythc'

Research Nodename:
-- ucr-rc-nautilus-research-node-forsythc--1-njq66

-------------------------------------------------------
```

This will also give you the workstation's name (nodename) 

```bash
kubectl get jobs
kubectl get pods
```

```bash
NAME                         COMPLETIONS   DURATION   AGE
forsythc-research-lab-1008   0/1           64s        64s
```
In the exmaple above the Research Workstation Name (nodename/jobname) = forsythc-research-lab-1008

## Connect to Research Node

```bash
kubectl exec -it nodename -- bash
```

## Upload data

```bash
kubectl cp localfile nodename:.
```

## Download data

```bash
kubectl cp nodename:./remotefile .
```

## Delete Research Node

```bash
kubectl delete jobs forsythc-research-lab-1008
```

### Trouble

From pod list, check log:

```bash
kubectl logs nodename 
```

Jobs and pods will expire after 1 week, however you can alter this with the following:

```yml
ttlSecondsAfterFinished=604800
```

Check on the Research Node details:

```bash
kubectl describe pod nodename 
```


## Links

* Help - https://element.nrp-nautilus.io
* Resources - https://nautilus.optiputer.net/resources
* Monitoring - https://grafana.nautilus.optiputer.net
