#!/bin/sh
# Backup script from kubectl

# Docker backup command.
BKPDIR=/backup/influxdb_$(date '+%Y-%m-%d_%H-%M')
PODNAME=$(kubectl get pods -o=name | grep influxdb | sed "s/^.\{4\}//")
TOKEN=2Kr5YuNWZ_Pq8QpT4663bsIchaTFxsiLDbjNNOgRi0Q8VwQigNWV8zaK0qV57gDAmaTcE7Dy0D10LAlFTP_dgw==

kubectl exec -it $PODNAME -- influx backup $BKPDIR -t $TOKEN
