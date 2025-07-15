ETL is divided into 6 individual steps separated with comments:<br>
-setup<br>
-filling empty coordinates in hotels data<br>
-add geocash to hotel and weather data<br>
-joining hotel and weather data<br>
-encryption of PII data<br>
-storing data<br>

Connecting to OpenCage API might fail, due to usage limitations, after a set number of invocations it returns 402 status responce.

Usage guide:
1. Follow https://git.epam.com/epmc-bdcc/trainings/bd201/m06_sparkbasics_python_azure project README instructions strictly, up to step 8. After completing those instructions, you should have already configured and running:
  - Resource Group:
  <img width="782" height="173" alt="image" src="https://github.com/user-attachments/assets/d63fc551-a534-4e15-9171-2477cd9ce982" />
  - Container Registry, Kubernetes Service and Storage Account within that Resource Group:
  <img width="961" height="201" alt="image" src="https://github.com/user-attachments/assets/ffda376b-2fb0-4a5e-b94f-8f76532b088a" />
  - Data injected to "data" Container on your Storage Account:
  <img width="667" height="499" alt="image" src="https://github.com/user-attachments/assets/47e1a7be-18c1-413d-91be-999c7b9a42e3" />

  
3. Launch Spark app with spark_submit.sh script, and remember to replace placeholders with actual secrets and adjust paths. Script is mostly spark-submit configuration from README mentioned above, but with additional environment variables. Remember also to delete pod with `kubectl delete pod <POD_NAME>`, if you are launching app again.
4. Verify logs with `kubectl logs <POD_NAME>`.
5. Verify result data under "data" container on Azure Storage. There should be additional directory called "enriched_data" with data prcessed by your ETL job.

Issues section:<br>
1. Issue with building docker image after corrections:<br>
Problem:<br>
After building a docker image and deploying it to AKS, it threw me an error, saying that it is not able to resolve environment variable froma main.py file line 12:  <br>
`f"fs.azure.account.key.{app_config['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net",`<br>
After code adjustments, image didn't use new version of code, even thought I rebuild egg file, checked if it contains correct version of code, rebuild docker image with --no-cache flag on and pushed it again on AKS.
Solution:<br>
TBD
