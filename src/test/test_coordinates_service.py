
from src.main.python.services.coordinates_service import CoordinatesService
from pyspark.sql import SparkSession



def test_fill_null_lat_lng_with_local_csv():
    spark = SparkSession.builder \
            .master("local[1]") \
            .appName("PII Encryption Test") \
            .getOrCreate()
    csv_path = 'src/test/resources/test_data_hotel_null_lat_lng.csv'
    df_hotels = spark\
        .read.option("header", True).csv(csv_path)\
        .withColumnRenamed("Latitude", "lat")\
        .withColumnRenamed("Longitude", "lng")
        
    coordinates_service = CoordinatesService()
    df_result = coordinates_service.fill_null_lat_lng(df_hotels)

    null_lat_count = df_result.filter(df_result['lat'].isNull()).count()
    null_lng_count = df_result.filter(df_result['lng'].isNull()).count()

    assert null_lat_count == 0, 'Latitude have null values'
    assert null_lng_count == 0, 'Longitude have null values'
    