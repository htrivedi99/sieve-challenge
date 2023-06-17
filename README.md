## How to run the project

### There are 4 components that you need to run on kuberentes
1. Redis
2. Celery runner
3. Core API
4. ML Model

Redis setup:
* Go into the redis directory and run the following commands
1. kubectl create -f sc.yaml
2. kubectl create -f pv.yaml
3. kubectl create -f redis-configmap.yaml
4. kubectl create -f redis-statefulset.yaml
5. kubectl create -f redis-service.yaml

Installing Metrics Server(Needed for horizontal pod autoscaler):
1. kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
2. kubectl edit deploy -n kube-system metrics-server
3. Set the arguments to the following:
```
   args:
     - --kubelet-insecure-tls
     - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
   
```


Celery setup:
* Go into the celery-task-queue/celery_runner directory and run the following commands
1. kubectl create -f deploy.yaml
2. kubectl create -f hpa.yaml

Core API setup:
* Go into the celery-task-queue/core_api directory and run the following commands
1. kubectl create -f deploy.yaml

ML Model setup:
* Go into the celery-task-queue/ml_models directory and run the following commands
1. kubectl create -f deploy.yaml
2. kubectl create -f hpa.yaml