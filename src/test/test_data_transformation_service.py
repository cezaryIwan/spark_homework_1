import pygeohash
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.main.python.services.data_transformation_service import DataTransformationService

@pytest.fixture(scope='module')
def spark():
    return SparkSession.builder.master('local[1]').appName('Test').getOrCreate()

@pytest.fixture(scope='module')
def data_transformation_service():
    return DataTransformationService(spark)

def test_add_geohash_lat_lng_creates_correct_hash(spark, data_transformation_service):
    csv_path = 'src/test/resources/test_data_hotel.csv'
    
    df = spark\
        .read.option("header", True).csv(csv_path)\
        .withColumnRenamed("Latitude", "lat")\
        .withColumnRenamed("Longitude", "lng")\
        .withColumn('lat', col('lat').cast('double'))\
        .withColumn('lng', col('lng').cast('double'))

    df_with_hash = data_transformation_service.add_geohash_lat_lng(df)

    assert 'geohash' in df_with_hash.columns

    row = df_with_hash.select('lat', 'lng', 'geohash').first()
    expected_hash = pygeohash.encode(row['lat'], row['lng'], precision=4)

    assert row['geohash'] == expected_hash
    
def test_join_hotels_with_weather_by_geohash(spark, data_transformation_service):

    hotels_df = spark\
        .read.option("header", True)\
        .csv("src/test/resources/test_data_hotel_geohash.csv", inferSchema=True)
        
    weather_df = spark\
        .read.option("header", True)\
        .csv("src/test/resources/test_data_weather.csv", inferSchema=True)

    result_df = data_transformation_service.join_hotels_with_weather_by_geohash(hotels_df, weather_df)

    result = {row["address"]: (row["temperature"], row["humidity"]) for row in result_df.collect()}

    assert result["10 Downing Street, London"] == (25.0, 0.60)
    assert result["Champs-Élysées, Paris"] == (26.0, 0.65)