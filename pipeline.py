#!/usr/bin/python3

####### Load modules ##########
import subprocess
from subprocess import Popen, PIPE
import time
import os
import sys
import argparse
import random
import configparser

###### Variables ###############
container = "gitlab-registry.nrp-nautilus.io/forsythc/container-blast"

###### Functions ################

def submit_job(jobname, container, command):
    submitresult = subprocess.Popen(["./pipeline.sh", jobname, container, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = submitresult.communicate()
    podname = monitor_job(jobname)
    podlogs = get_pod_logs(podname)
    clean_up_job(jobname)
    #print(podlogs)
    return podlogs
    #return jobname

    

def monitor_job(jobname):
    print("Running job: %s ... " %(jobname))
    while True:
        cmd = "kubectl get pods --no-headers --selector=job-name=%s | grep 'Complete' | awk '{print $1}'" % (jobname)
        cmdresult = subprocess.Popen(["/bin/sh", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, err = cmdresult.communicate()
        result = result.rstrip()
        time.sleep(5)
        if not result:
            #print("%s still running" %(jobname))
            pass
        else:
            #print("Complete")
            return result

def get_pod_logs(podname):
    cmd = "kubectl logs %s" % (podname)
    cmdresult = subprocess.Popen(["/bin/sh", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = cmdresult.communicate()
    return result

def clean_up_job(jobname):
    cmd = "kubectl delete jobs %s" % (jobname)
    cmdresult = subprocess.Popen(["/bin/sh", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = cmdresult.communicate()


def load_pipeline_config():
    pipelineconfig = configparser.RawConfigParser()
    pipelineconfigFilePath = r'pipeline.conf'
    pipelineconfig.read(pipelineconfigFilePath)
    pipelineconfig_dict = dict(pipelineconfig.items('pipeline-series'))
    print(dict(pipelineconfig.items('pipeline-series')))
    return pipelineconfig_dict

def run_pipeline_config_dict(pipelineconfig_dict, container):
    for step, cmd in pipelineconfig_dict.items():
        #print("running %s and it looks like %s" % (step,cmd))
        submit_job(step, container, cmd)

def run_pipeline_config_dict_parallel(pipelineconfig_dict, container):
    for step, cmd in pipelineconfig_dict.items():
        #print("running %s and it looks like %s" % (step,cmd))
        submit_job_parallel(step, container, cmd)
        print("%s launched .." % (step))

def submit_job_parallel(jobname, container, command):
    submitresult = subprocess.Popen(["./pipeline.sh", jobname, container, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = submitresult.communicate()


########## Main Code ##########

if __name__ == '__main__':

####### One job catch output  #############
    #joboutput = submit_job("test", container, "uptime")

####### Sample Jobs    #########
    #print(submit_job("job1", container, "ls -latr /sharedvol/ursa-data-connect-input"))
    #print(submit_job("job2", container, "cp /sharedvol/ursa-data-connect-input/zebrafish.top.faa .; cp /sharedvol/ursa-data-connect-input/mouse.1.protein.faa .;cp /sharedvol/ursa-data-connect-input/zebrafish.1.protein.faa .; ./makeblastdb -in mouse.1.protein.faa -dbtype prot; ./makeblastdb -in zebrafish.1.protein.faa -dbtype prot; ./blastp -query zebrafish.top.faa -db mouse.1.protein.faa -num_threads 4 -out zebrafish.x.mouse;tar -zcvf job-output.tar.gz zebrafish.x.mouse;cp job-output.tar.gz /sharedvol/$(hostname)job-output.tar.gz"))

###### Uses config file for job list   ######
    pipelineconfig_dict = load_pipeline_config()
    #run_pipeline_config_dict(pipelineconfig_dict,container)
    #run_pipeline_config_dict(load_pipeline_config(),container)
    run_pipeline_config_dict_parallel(load_pipeline_config(),container)

######## Simple Series of jobs that act on data in a shared location ########
    #print(submit_job("step1", container, "ls -latr /sharedvol/"))
    #print(submit_job("step2", container, "touch /sharedvol/testfile"))
    #print(submit_job("datatime1", container, "echo 'data1' >> /sharedvol/testfile"))
    #print(submit_job("datatime2", container, "echo 'data2' >> /sharedvol/testfile"))
    #print(submit_job("datatime3", container, "echo 'data3' >> /sharedvol/testfile"))
    #print(submit_job("cattheresults", container, "cat /sharedvol/testfile"))
    #print(submit_job("cleanup", container, "rm -f /sharedvol/testfile"))

######## Running other containers #########
    #print(submit_job("busybox", "busybox", "ls /sharedvol/"))
    #print(submit_job("centos", "centos", "cat /etc/os-release"))
    #print(submit_job("ubuntu", "ubuntu", "cat /etc/os-release"))

#######  Fire and Forget #####
    #submit_job_parallel("busybox1", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox2", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox3", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox4", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox5", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox6", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox7", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("busybox8", "busybox", "echo $(hostname) >> /sharedvol/testfile")

    #submit_job_parallel("xyzbusybox1", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox2", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox3", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox4", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox5", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox6", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox7", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzbusybox8", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #print(submit_job("xyzstep1", container, "ls -latr /sharedvol/"))
    #print(submit_job("xyzstep2", container, "touch /sharedvol/testfile"))
    #print(submit_job("xyzdatatime1", container, "echo 'data1' >> /sharedvol/testfile"))
    #print(submit_job("xyzdatatime2", container, "echo 'data2' >> /sharedvol/testfile"))
    #print(submit_job("xyzdatatime3", container, "echo 'data3' >> /sharedvol/testfile"))
    #print(submit_job("xyzcattheresults", container, "cat /sharedvol/testfile"))
    #print(submit_job("xyzcleanup", container, "rm -f /sharedvol/testfile"))
    #print(submit_job("xyzbusybox", "busybox", "ls /sharedvol/"))
    #print(submit_job("xyzcentos", "centos", "cat /etc/os-release"))
    #print(submit_job("xyzubuntu", "ubuntu", "cat /etc/os-release"))
    #submit_job_parallel("xyzrbusybox1", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox2", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox3", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox4", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox5", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox6", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox7", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #submit_job_parallel("xyzrbusybox8", "busybox", "echo $(hostname) >> /sharedvol/testfile")
    #print(submit_job("xyzcleanup", container, "rm -f /sharedvol/testfile"))
    #print(submit_job("xyzcleanup", container, "rm -f /sharedvol/zzz*"))

    exit()









