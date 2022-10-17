#!/usr/bin/sh 

jobname="$1"
jobcontainer="$2"
jobcommand="$3"


cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: $jobname
  labels:
    jobtype: pipeline
spec:
  template:
    spec:
      containers:
      - name: $jobname
        image: $jobcontainer
        command:
        - sh
        - -c
        - "$jobcommand"
        volumeMounts:
        - mountPath: /sharedvol
          name: sharedvol
        resources:
          limits:
            memory: 6Gi
            cpu: "4"
          requests:
            memory: 100Mi
            cpu: "10m"
      volumes:
      - name: sharedvol
        persistentVolumeClaim:
          claimName: master-vol
      - name: git-repo
        emptyDir: {}
      restartPolicy: Never
  backoffLimit: 1
EOF
