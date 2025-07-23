ETL is divided into 6 individual steps separated with comments:<br>
-setup<br>
-filling empty coordinates in hotels data<br>
-add geocash to hotel and weather data<br>
-joining hotel and weather data<br>
-encryption of PII data<br>
-storing data<br>

Connecting to OpenCage API might fail, due to usage limitations, after a set number of invocations it returns 402 status responce. <br>

Setup: <br>
1. `terraform destroy`: <br>
```
(venv) cezary@ubuntuserver:~/spark_homeworks/m06_sparkbasics_python_azure/terraform$ terraform destroy
Acquiring state lock. This may take a few moments...
random_string.suffix: Refreshing state... [id=ykw2]
data.azurerm_client_config.current: Reading...
azurerm_resource_group.bdcc: Refreshing state... [id=/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2]
data.azurerm_client_config.current: Read complete after 0s [id=Y2xpZW50Q29uZmlncy9jbGllbnRJZD0wNGIwNzc5NS04ZGRiLTQ2MWEtYmJlZS0wMmY5ZTFiZjdiNDY7b2JqZWN0SWQ9MDk0YTQxZWUtYzFkYy00Y2M2LTgwYTctN2JkYWIzN2Y0MTM2O3N1YnNjcmlwdGlvbklkPTc5MDg3NTU2LTIyYWMtNDY2Ny1hMDhlLWUzZDgyNmQxOGU1NDt0ZW5hbnRJZD1lNTYzNTA4ZS02OTYyLTRmODYtOWE5OC1mN2JhOTViYTk1ZTU=]
azurerm_container_registry.acr: Refreshing state... [id=/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2/providers/Microsoft.ContainerRegistry/registries/acrdevwesteuropeykw2]
azurerm_storage_account.bdcc: Refreshing state... [id=/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2/providers/Microsoft.Storage/storageAccounts/stdevwesteuropeykw2]
azurerm_kubernetes_cluster.bdcc: Refreshing state... [id=/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2/providers/Microsoft.ContainerService/managedClusters/aks-dev-westeurope-ykw2]
azurerm_storage_data_lake_gen2_filesystem.gen2_data: Refreshing state... [id=https://stdevwesteuropeykw2.dfs.core.windows.net/data]
azurerm_role_assignment.aks_acr_pull: Refreshing state... [id=/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2/providers/Microsoft.ContainerRegistry/registries/acrdevwesteuropeykw2/providers/Microsoft.Authorization/roleAssignments/b46e3b54-cfc9-62e1-5733-46def57d03d1]
kubernetes_service_account.spark: Refreshing state... [id=default/spark]
kubernetes_cluster_role.spark_role: Refreshing state... [id=spark-role]
kubernetes_cluster_role_binding.spark_role_binding: Refreshing state... [id=spark-role-binding]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # azurerm_container_registry.acr will be destroyed
  - resource "azurerm_container_registry" "acr" {
      - admin_enabled                 = false -> null
      - anonymous_pull_enabled        = false -> null
      - data_endpoint_enabled         = false -> null
      - encryption                    = [] -> null
      - export_policy_enabled         = true -> null
      - id                            = "/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2/providers/Microsoft.ContainerRegistry/registries/acrdevwesteuropeykw2" -> null

...

azurerm_kubernetes_cluster.bdcc: Still destroying... [id=/subscriptions/79087556-22ac-4667-a08e-...anagedClusters/aks-dev-westeurope-ykw2, 04m21s elapsed]
azurerm_kubernetes_cluster.bdcc: Still destroying... [id=/subscriptions/79087556-22ac-4667-a08e-...anagedClusters/aks-dev-westeurope-ykw2, 04m31s elapsed]
azurerm_kubernetes_cluster.bdcc: Destruction complete after 4m34s
azurerm_resource_group.bdcc: Destroying... [id=/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/rg-dev-westeurope-ykw2]
azurerm_resource_group.bdcc: Still destroying... [id=/subscriptions/79087556-22ac-4667-a08e-.../resourceGroups/rg-dev-westeurope-ykw2, 00m10s elapsed]
azurerm_resource_group.bdcc: Still destroying... [id=/subscriptions/79087556-22ac-4667-a08e-.../resourceGroups/rg-dev-westeurope-ykw2, 00m20s elapsed]
azurerm_resource_group.bdcc: Still destroying... [id=/subscriptions/79087556-22ac-4667-a08e-.../resourceGroups/rg-dev-westeurope-ykw2, 00m30s elapsed]
azurerm_resource_group.bdcc: Still destroying... [id=/subscriptions/79087556-22ac-4667-a08e-.../resourceGroups/rg-dev-westeurope-ykw2, 00m40s elapsed]
azurerm_resource_group.bdcc: Destruction complete after 46s
random_string.suffix: Destroying... [id=ykw2]
random_string.suffix: Destruction complete after 0s
Releasing state lock. This may take a few moments...

Destroy complete! Resources: 10 destroyed.

```
2. Destroy remaining resources on cloud: <br>
<img width="1063" height="200" alt="image" src="https://github.com/user-attachments/assets/d2f9b7b2-958e-463e-afd3-0bcf9f9925a1" /> <br>


3. `az group create --name sparkhm1 --location polandcentral`: <br>
```

{
  "id": "/subscriptions/79087556-22ac-4667-a08e-e3d826d18e54/resourceGroups/sparkhm1",
  "location": "polandcentral",
  "managedBy": null,
  "name": "sparkhm1",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}

```
4. `az storage account create --name hwsparkcezarysa --resource-group sparkhm1 --location polandcentral --sku Standard_LRS`: <br>
```

/opt/az/lib/python3.12/site-packages/azure/multiapi/storagev2/fileshare/__init__.py:1: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
{
  "accessTier": "Hot",

...

  "type": "Microsoft.Storage/storageAccounts"
}
```
5.  `az storage container create --name hwsparkcezarycontainer --account-name hwsparkcezarysa`: <br>
```

/opt/az/lib/python3.12/site-packages/azure/multiapi/storagev2/fileshare/__init__.py:1: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)

There are no credentials provided in your command and environment, we will query for account key for your storage account.
It is recommended to provide --connection-string, --account-key or --sas-token in your command as credentials.

You also can add `--auth-mode login` in your command to use Azure Active Directory (Azure AD) for authorization if your login account is assigned required RBAC roles.
For more information about RBAC roles in storage, visit https://learn.microsoft.com/azure/storage/common/storage-auth-aad-rbac-cli.

In addition, setting the corresponding environment variables can avoid inputting credentials in your command. Please use --help to get more information about environment variable usage.
{
  "created": true
}

```
6. Fill placeholders in main.tf file
7. `terraform init`: <br>
<img width="689" height="326" alt="image" src="https://github.com/user-attachments/assets/d1e40a97-21ba-4781-97da-1bffd47871c7" /> <br>
8. `terraform plan -out terraform.plan`: <br>
<img width="561" height="105" alt="image" src="https://github.com/user-attachments/assets/1cf6c212-3203-4250-82ae-4b246ea09710" /> <br>
9. `terraform apply terraform.plan`: <br>
<img width="606" height="155" alt="image" src="https://github.com/user-attachments/assets/a14660ff-a09d-40cb-a3ac-8d7872c682f8" /> <br>
10. List resource groups with creation time (simple grouping bash command, made by AI chat): <br>
<img width="950" height="110" alt="image" src="https://github.com/user-attachments/assets/dac48cfc-af7f-46d1-af9d-dfce99e2b830" /> <br>
11. ACR login: <br>
<img width="982" height="58" alt="image" src="https://github.com/user-attachments/assets/d265ecd7-6172-450c-906a-94ddbc8a7598" /> <br>
12. Upload files to 'data' container: <br>
<img width="331" height="362" alt="image" src="https://github.com/user-attachments/assets/94c0952c-9c08-4f9b-bea8-96845d674795" /> <br>
13. Create python venv: <br>
<img width="677" height="66" alt="image" src="https://github.com/user-attachments/assets/48822be6-3f89-4d43-b311-112e24c0eb21" /> <br>

--- AT THIS POINT DEVELOP AND TEST YOUR ETL AND THEN MOVE ON ---

14. Install requirements.txt (I updated requirements after completion of ETL with freeze > requirements.txt): <br>
```

(venv) cezary@ubuntuserver:~/spark_homeworks/m06_sparkbasics_python_azure$ pip install -r requirements.txt
Collecting aiohappyeyeballs==2.6.1 (from -r requirements.txt (line 1))
  Using cached aiohappyeyeballs-2.6.1-py3-none-any.whl.metadata (5.9 kB)

...

Installing collected packages: py4j, wheel, urllib3, tqdm, setuptools, python-dotenv, pyspark, Pygments, pygeohash, propcache, pluggy, packaging, multidict, iniconfig, idna, frozenlist, charset-normalizer, certifi, backoff, attrs, aiohappyeyeballs, yarl, requests, pytest, dotenv, aiosignal, aiohttp, opencage
Successfully installed Pygments-2.19.2 aiohappyeyeballs-2.6.1 aiohttp-3.12.12 aiosignal-1.3.2 attrs-25.3.0 backoff-2.2.1 certifi-2025.4.26 charset-normalizer-3.4.2 dotenv-0.9.9 frozenlist-1.7.0 idna-3.10 iniconfig-2.1.0 multidict-6.4.4 opencage-3.2.0 packaging-25.0 pluggy-1.6.0 propcache-0.3.2 py4j-0.10.9.9 pygeohash-3.1.3 pyspark-4.0.0 pytest-8.4.1 python-dotenv-1.1.1 requests-2.32.4 setuptools-80.9.0 tqdm-4.67.1 urllib3-2.4.0 wheel-0.45.1 yarl-1.20.1

```
15. `python3 setup.py bdist_egg`: <br>
```

running bdist_egg
running egg_info
writing src/sparkbasics.egg-info/PKG-INFO
writing dependency_links to src/sparkbasics.egg-info/dependency_links.txt
writing top-level names to src/sparkbasics.egg-info/top_level.txt

...

byte-compiling build/bdist.linux-x86_64/egg/test/test_encryption_service.py to test_encryption_service.cpython-312.pyc
creating build/bdist.linux-x86_64/egg/EGG-INFO
copying src/sparkbasics.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
copying src/sparkbasics.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying src/sparkbasics.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying src/sparkbasics.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
copying src/sparkbasics.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
creating 'dist/sparkbasics-1.0.0-py3.12.egg' and adding 'build/bdist.linux-x86_64/egg' to it
removing 'build/bdist.linux-x86_64/egg' (and everything under it)

```

Issues section:<br>
1. Issue with building docker image after corrections:<br>
Problem summary:<br>
After building a docker image and deploying it to AKS, it threw me an error, saying that it is not able to resolve environment variable from main.py file line 12:  <br>
`f"fs.azure.account.key.{config['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net",`<br>
After code adjustments and changing name of config file to app_config: <br>
`f"fs.azure.account.key.{app_config['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net",` <br>
image didn't use new version of code, even thought I rebuild egg file, checked if it contains correct version of code, rebuild docker image with --no-cache flag on and pushed it again on AKS. <br>

Steps:
1. Follow "Setup" section from above, this way you should have already created .egg file of your ETL
2. Verified .egg contents: <br>
`unzip -d /tmp/egg_out docker/dist/sparkbasics-*.egg`
<img width="885" height="334" alt="image" src="https://github.com/user-attachments/assets/3732e8ae-ad41-4ba1-991a-7908c34effb7" /> <br>
Here we can see updated version of code with app_config name, not config, which will be thrown in k8s pod's logs later. <br>
3. Build Docker image using command from project's repository with additional --no-cache flag, to ensure newly generated .egg file is used (rememver to move or copy "requirements.txt" to "docker" folder): <br>

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
<br>
Working with completed ETL on cloud: <br>
1. Set node pool to autoscale, as 1 node was not sufficient: <br>
<img width="565" height="455" alt="image" src="https://github.com/user-attachments/assets/eace7e1e-e704-4daf-af4e-fb6463d150ba" /> <br>
2. Autoscale tried to use more than 2 nodes, which was too much for my subscription's quota: <br>
<img width="1838" height="599" alt="image" src="https://github.com/user-attachments/assets/7445d90c-176c-4975-aafc-f253585c1b0e" /> <br>
3. Set node cout to 2, and disabled autoscaling since I cannot go for more than 2 nodes anyway and don't need azure to scale down for this exercise: <br>
<img width="640" height="524" alt="image" src="https://github.com/user-attachments/assets/c4bf6e2a-fc6c-4dda-86a3-65b94f2b45fa" /> <br>
4. Now spark do not see my services, in built  image: <br>

```

  File "/opt/spark/python/lib/pyspark.zip/pyspark/serializers.py", line 472, in loads
    return cloudpickle.loads(obj, encoding=encoding)
ModuleNotFoundError: No module named 'services'

``` 

<br>
5. I might adjust path i setup.py, adjust submit script and keep shorter imports, but I don't mind longer imports on this homework so I will adjust paths in my python files e.g.: <br>
<img width="796" height="188" alt="image" src="https://github.com/user-attachments/assets/64d1bae2-8d34-4206-bd05-a685fa3d2e22" /> <br>
6. After building image and running it on AKS, still exactly the same error from 4. is thrown, unzipping and checking .egg file: <br>
<img width="1032" height="47" alt="image" src="https://github.com/user-attachments/assets/e7c551c8-e46d-4424-875d-1c2eb37a7896" /> <br>
<img width="812" height="209" alt="image" src="https://github.com/user-attachments/assets/d0edd44b-801e-4475-9215-1dcba13ce993" /> <br>
7. .egg from local files seems fine, checking files from faulty pod: <br>
<img width="1089" height="75" alt="image" src="https://github.com/user-attachments/assets/7ecd0945-c4a1-4b07-bde9-670cb05b138c" /> <br>
<img width="698" height="52" alt="image" src="https://github.com/user-attachments/assets/dd50295c-c454-46b1-821f-88bf190855b7" /> <br>
<img width="1206" height="36" alt="image" src="https://github.com/user-attachments/assets/0b767f5b-3d48-4cbc-ae73-79332d3c1c83" /> <br>
<img width="757" height="44" alt="image" src="https://github.com/user-attachments/assets/edea75cc-95a9-45a2-9579-6e42eec0e0a4" /> <br>
<img width="742" height="153" alt="image" src="https://github.com/user-attachments/assets/021955ac-a13e-4036-be26-6c33cdddb575" /> <br>
8. pod on AKS have falty, not updated version of code, checking image i built locally:  <br>
<img width="844" height="59" alt="image" src="https://github.com/user-attachments/assets/8fef9c95-6473-49fd-ae3c-c88fb7166c06" /> <br>
<img width="846" height="59" alt="image" src="https://github.com/user-attachments/assets/82584945-3ed9-4ca8-8ac3-7842159a0127" /> <br>
<img width="849" height="73" alt="image" src="https://github.com/user-attachments/assets/9186b09d-bac0-4f8c-be92-e3c5968f9556" /> <br>
<img width="788" height="152" alt="image" src="https://github.com/user-attachments/assets/0a8a5fb2-6ebd-44a1-aa21-b3af3c5c7c9b" /> <br>
9. Local image is fine, checking image on ACR:  <br>
<img width="842" height="109" alt="image" src="https://github.com/user-attachments/assets/606a54e7-1f6d-4973-ac61-19071514ddd5" /> <br>
My image locally and on ACR have identical "digest", so they have to be identical itself - for some reason, I have updated image on registry, but AKS is using an obsolited image. It would make sense, that after recreation of infra it worked, as I assume AKS uses cached image with faulty code <br>
10. Trying submitting with forced pulling: <br>
<img width="809" height="38" alt="image" src="https://github.com/user-attachments/assets/e318778b-b1cb-4653-8534-a9b5ac73a273" /> <br>







