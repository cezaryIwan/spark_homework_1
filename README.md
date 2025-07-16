ETL is divided into 6 individual steps separated with comments:<br>
-setup<br>
-filling empty coordinates in hotels data<br>
-add geocash to hotel and weather data<br>
-joining hotel and weather data<br>
-encryption of PII data<br>
-storing data<br>

Connecting to OpenCage API might fail, due to usage limitations, after a set number of invocations it returns 402 status responce.

Usage guide:
1. Follow https://git.epam.com/epmc-bdcc/trainings/bd201/m06_sparkbasics_python_azure project README instructions strictly, up to step 8. After completing those instructions, you should have already configured and running: <br>
  - Resource Group: <br>
  <img width="782" height="173" alt="image" src="https://github.com/user-attachments/assets/d63fc551-a534-4e15-9171-2477cd9ce982" /> <br>
  - Container Registry, Kubernetes Service and Storage Account within that Resource Group: <br>
  <img width="961" height="201" alt="image" src="https://github.com/user-attachments/assets/ffda376b-2fb0-4a5e-b94f-8f76532b088a" /> <br>
  - Data injected to "data" Container on your Storage Account: <br>
  <img width="667" height="499" alt="image" src="https://github.com/user-attachments/assets/47e1a7be-18c1-413d-91be-999c7b9a42e3" /> <br>

  
3. Launch Spark app with spark_submit.sh script, and remember to replace placeholders with actual secrets and adjust paths. Script is mostly spark-submit configuration from README mentioned above, but with additional environment variables. Remember also to delete pod with `kubectl delete pod <POD_NAME>`, if you are launching app again. <br>
4. Verify logs with `kubectl logs <POD_NAME>`. <br>
5. Verify result data under "data" container on Azure Storage. There should be additional directory called "enriched_data" with data prcessed by your ETL job. <br>

Issues section:<br>
1. Issue with building docker image after corrections:<br>
Problem summary:<br>
After building a docker image and deploying it to AKS, it threw me an error, saying that it is not able to resolve environment variable from main.py file line 12:  <br>
`f"fs.azure.account.key.{config['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net",`<br>
After code adjustments and changing name of config file to app_config: <br>
`f"fs.azure.account.key.{app_config['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net",` <br>
image didn't use new version of code, even thought I rebuild egg file, checked if it contains correct version of code, rebuild docker image with --no-cache flag on and pushed it again on AKS. <br>

Steps:
1. Starting with empty /docker/dist folder, so I'm sure .egg file is freshly generated. <br>
<img width="537" height="294" alt="image" src="https://github.com/user-attachments/assets/0c63f7da-c6fa-4428-b01a-345deb0ac97b" /> <br>
Ran the following command to generate the .egg file: <br>
`python3 setup.py bdist_egg`
Result: <br>
<img width="437" height="269" alt="image" src="https://github.com/user-attachments/assets/3e603ab8-c330-4af5-80d0-d67e79042541" /> <br>
2. Verified .egg contents: <br>
`unzip -d /tmp/egg_out docker/dist/sparkbasics-*.egg`
<img width="885" height="334" alt="image" src="https://github.com/user-attachments/assets/3732e8ae-ad41-4ba1-991a-7908c34effb7" /> <br>
Here we can see updated version of code with app_config name, not config, which will be thrown in k8s pod's logs later. <br>
3. Build Docker image using command from project's repository with additional --no-cache flag, to ensure newly generated .egg file is used: <br>

```bash
docker build \
  --no-cache \
  -t acrdevwesteuropeykw2.azurecr.io/spark-python-06:v2 \
  -f docker/Dockerfile \
  docker/ --build-context extra-source=./
```

  Result: <br>
<img width="1375" height="691" alt="image" src="https://github.com/user-attachments/assets/92c02be9-28d4-48bd-9ab5-5a0b5cbe4436" /> <br>

4. Ensured correct format of scripts:
`dos2unix docker/*.sh`  <br>
Result:
<img width="721" height="62" alt="image" src="https://github.com/user-attachments/assets/4b923a66-9237-4bf0-983f-4763480de323" />  <br>
5. Logged in to Azure Container Registry:  <br>
`az acr login --name acrdevwesteuropeykw2`  <br>
Result: <br>
<img width="901" height="82" alt="image" src="https://github.com/user-attachments/assets/2e7034fb-3d2c-40a9-89bc-1d592a556d8a" /> <br>
6. Pushed the image to ACR: <br>
`docker push acrdevwesteuropeykw2.azurecr.io/spark-python-06:v2` <br>
Result: <br>
<img width="999" height="328" alt="image" src="https://github.com/user-attachments/assets/3ec6f784-3b3f-4702-8b9c-42c6a2104978" /> <br>
7. Checked if depreciated pods already exists and if so, deleted them: <br>
<img width="782" height="173" alt="image" src="https://github.com/user-attachments/assets/1249a009-d0df-456b-956c-5b6651b3276b" /> <br>

8. Ran the Spark job via Kubernetes using the spark_submit.sh script (https://github.com/cezaryIwan/spark_homework_1/blob/master/spark_submit.sh), with container.image property correctly set, in this case: <br>
`    --conf spark.kubernetes.container.image=acrdevwesteuropeykw2.azurecr.io/spark-python-06:v2 \` <br>
Result: <br>

```bash
(venv) cezary@ubuntuserver:~/spark_homeworks/m06_sparkbasics_python_azure$ ./spark_submit.sh 
WARNING: Using incubator modules: jdk.incubator.vector
25/07/16 13:07:10 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
25/07/16 13:07:10 INFO SparkKubernetesClientFactory: Auto-configuring K8S client using current context from users K8S config file
25/07/16 13:07:14 INFO KerberosConfDriverFeatureStep: You have not specified a krb5.conf file locally or via a ConfigMap. Make sure that you have the krb5.conf locally on the driver image.
25/07/16 13:07:20 INFO LoggingPodStatusWatcherImpl: State changed, new state: 
         pod name: spark-driver
         namespace: default
         labels: spark-app-name -> sparkbasics, spark-app-selector -> spark-b2332fe807f64c5b9fa50852f9f88a68, spark-role -> driver, spark-version -> 4.0.0
         pod uid: 95aa87a4-28a0-4922-9d32-bc9d3079dc7f
         creation time: 2025-07-16T13:07:19Z
         service account name: spark
         volumes: spark-local-dir-1, spark-conf-volume-driver, kube-api-access-n95jk
         node name: aks-default-21166179-vmss000001
         start time: 2025-07-16T13:07:19Z
         phase: Pending
         container status: 
                 container name: spark-kubernetes-driver
                 container image: acrdevwesteuropeykw2.azurecr.io/spark-python-06:latest
                 container state: waiting
                 pending reason: ContainerCreating
25/07/16 13:07:20 INFO LoggingPodStatusWatcherImpl: State changed, new state: 
         pod name: spark-driver
         namespace: default
         labels: spark-app-name -> sparkbasics, spark-app-selector -> spark-b2332fe807f64c5b9fa50852f9f88a68, spark-role -> driver, spark-version -> 4.0.0
         pod uid: 95aa87a4-28a0-4922-9d32-bc9d3079dc7f
         creation time: 2025-07-16T13:07:19Z
         service account name: spark
         volumes: spark-local-dir-1, spark-conf-volume-driver, kube-api-access-n95jk
         node name: aks-default-21166179-vmss000001
         start time: 2025-07-16T13:07:19Z
         phase: Pending
         container status: 
                 container name: spark-kubernetes-driver
                 container image: acrdevwesteuropeykw2.azurecr.io/spark-python-06:latest
                 container state: waiting
                 pending reason: ContainerCreating
25/07/16 13:07:20 INFO LoggingPodStatusWatcherImpl: Waiting for application sparkbasics} with application ID spark-b2332fe807f64c5b9fa50852f9f88a68 and submission ID default:spark-driver to finish...
25/07/16 13:07:21 INFO LoggingPodStatusWatcherImpl: Application status for spark-b2332fe807f64c5b9fa50852f9f88a68 (phase: Pending)
25/07/16 13:07:21 INFO LoggingPodStatusWatcherImpl: State changed, new state: 
         pod name: spark-driver
         namespace: default
         labels: spark-app-name -> sparkbasics, spark-app-selector -> spark-b2332fe807f64c5b9fa50852f9f88a68, spark-role -> driver, spark-version -> 4.0.0
         pod uid: 95aa87a4-28a0-4922-9d32-bc9d3079dc7f
         creation time: 2025-07-16T13:07:19Z
         service account name: spark
         volumes: spark-local-dir-1, spark-conf-volume-driver, kube-api-access-n95jk
         node name: aks-default-21166179-vmss000001
         start time: 2025-07-16T13:07:19Z
         phase: Running
         container status: 
                 container name: spark-kubernetes-driver
                 container image: acrdevwesteuropeykw2.azurecr.io/spark-python-06:latest
                 container state: running
                 container started at: 2025-07-16T13:07:21Z
25/07/16 13:07:22 INFO LoggingPodStatusWatcherImpl: Application status for spark-b2332fe807f64c5b9fa50852f9f88a68 (phase: Running)
25/07/16 13:07:23 INFO LoggingPodStatusWatcherImpl: Application status for spark-b2332fe807f64c5b9fa50852f9f88a68 (phase: Running)
25/07/16 13:07:24 INFO LoggingPodStatusWatcherImpl: Application status for spark-b2332fe807f64c5b9fa50852f9f88a68 (phase: Running)
...
25/07/16 13:08:03 INFO LoggingPodStatusWatcherImpl: State changed, new state: 
         pod name: spark-driver
         namespace: default
         labels: spark-app-name -> sparkbasics, spark-app-selector -> spark-b2332fe807f64c5b9fa50852f9f88a68, spark-role -> driver, spark-version -> 4.0.0
         pod uid: 95aa87a4-28a0-4922-9d32-bc9d3079dc7f
         creation time: 2025-07-16T13:07:19Z
         service account name: spark
         volumes: spark-local-dir-1, spark-conf-volume-driver, kube-api-access-n95jk
         node name: aks-default-21166179-vmss000001
         start time: 2025-07-16T13:07:19Z
         phase: Running
         container status: 
                 container name: spark-kubernetes-driver
                 container image: acrdevwesteuropeykw2.azurecr.io/spark-python-06:latest
                 container state: terminated
                 container started at: 2025-07-16T13:07:21Z
                 container finished at: 2025-07-16T13:08:03Z
                 exit code: 1
                 termination reason: Error
25/07/16 13:08:04 INFO LoggingPodStatusWatcherImpl: Application status for spark-b2332fe807f64c5b9fa50852f9f88a68 (phase: Running)
25/07/16 13:08:05 INFO LoggingPodStatusWatcherImpl: State changed, new state: 
         pod name: spark-driver
         namespace: default
         labels: spark-app-name -> sparkbasics, spark-app-selector -> spark-b2332fe807f64c5b9fa50852f9f88a68, spark-role -> driver, spark-version -> 4.0.0
         pod uid: 95aa87a4-28a0-4922-9d32-bc9d3079dc7f
         creation time: 2025-07-16T13:07:19Z
         service account name: spark
         volumes: spark-local-dir-1, spark-conf-volume-driver, kube-api-access-n95jk
         node name: aks-default-21166179-vmss000001
         start time: 2025-07-16T13:07:19Z
         phase: Failed
         container status: 
                 container name: spark-kubernetes-driver
                 container image: acrdevwesteuropeykw2.azurecr.io/spark-python-06:latest
                 container state: terminated
                 container started at: 2025-07-16T13:07:21Z
                 container finished at: 2025-07-16T13:08:03Z
                 exit code: 1
                 termination reason: Error
25/07/16 13:08:05 INFO LoggingPodStatusWatcherImpl: Application status for spark-b2332fe807f64c5b9fa50852f9f88a68 (phase: Failed)
25/07/16 13:08:05 INFO LoggingPodStatusWatcherImpl: Container final statuses:


         container name: spark-kubernetes-driver
         container image: acrdevwesteuropeykw2.azurecr.io/spark-python-06:latest
         container state: terminated
         container started at: 2025-07-16T13:07:21Z
         container finished at: 2025-07-16T13:08:03Z
         exit code: 1
         termination reason: Error
25/07/16 13:08:05 INFO LoggingPodStatusWatcherImpl: Application sparkbasics with application ID spark-b2332fe807f64c5b9fa50852f9f88a68 and submission ID default:spark-driver finished
25/07/16 13:08:05 INFO ShutdownHookManager: Shutdown hook called
25/07/16 13:08:05 INFO ShutdownHookManager: Deleting directory /tmp/spark-d2c17d74-8d18-4fcd-a792-a7f9adb8c49d
```
 <br>
Logs: <br>
<img width="1366" height="648" alt="image" src="https://github.com/user-attachments/assets/b1824747-4b27-4f40-9ec9-e42dc6847a84" /> <br>
<br>
It seems that for some reason spark job is using old version of code. I assume that, because logs the old name of config file is logged (config) not new one (app_cofing). <br>
Solution:<br>
TBD
