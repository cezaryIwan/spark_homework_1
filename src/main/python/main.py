from pyspark.sql import SparkSession
from app_config import app_config
from services.data_transformation_service import DataTransformationService
from services.coordinates_service import CoordinatesService
from services.encryption_service import EncryptionService

# Create Spark session
spark = SparkSession.builder.appName("Hotel-Weather ETL Job")\
.config("spark.jars.packages", "org.apache.hadoop:hadoop-azure:3.3.4,com.microsoft.azure:azure-storage:8.6.6")\
    .getOrCreate()
spark.conf.set(
    f"fs.azure.account.key.{app_config['AZURE_STORAGE_ACCOUNT_NAME']}.blob.core.windows.net",
    app_config['AZURE_STORAGE_ACCOUNT_KEY']
)

data_transformation_service = DataTransformationService(spark)
coordinates_service = CoordinatesService()
encryption_service = EncryptionService()

df_hotels = spark.read.option("header", True).csv(app_config['STORAGE_PATH'] + app_config['STORAGE_HOTELS_SUBPATH'] )
df_weather = spark.read.parquet(app_config['STORAGE_PATH'] + app_config['STORAGE_WEATHER_SUBPATH'] )
# To ensure consistency in column names and avoid dupliating values when joining with weather data
df_hotels = df_hotels\
            .withColumnRenamed("Latitude", "lat")\
            .withColumnRenamed("Longitude", "lng")

# Add missing coordinates to hotel data
df_hotels = coordinates_service.fill_null_lat_lng(df_hotels)

#Enrich by geohash
df_hotels = data_transformation_service.add_geohash_lat_lng(df_hotels)
df_weather = data_transformation_service.add_geohash_lat_lng(df_weather)

#Join weather and hotels
df_hotels_weather = data_transformation_service.join_hotels_with_weather_by_geohash(
    df_hotels,
    df_weather
    )

# Encrypt PII fields
df_hotels_weather_encrypted = encryption_service.encrypt_fields(
    df_hotels_weather,
    encryption_service.pii_fields()
)

#Store enriched data
df_hotels_weather_encrypted.write.mode("append").parquet(
    f"wasbs://{app_config['AZURE_CONTAINER_NAME']}@{app_config['AZURE_STORAGE_ACCOUNT_NAME'] }.blob.core.windows.net/enriched_data"
)


spark.stop()
