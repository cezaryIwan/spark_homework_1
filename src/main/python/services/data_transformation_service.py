import pygeohash
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

class DataTransformationService:

    def __init__(self, spark):
        self.spark = spark
    
    def add_geohash_lat_lng(self, df):
        return df.withColumn("geohash", self.geohash_4_udf(col("lat"), col("lng")))

    @staticmethod
    @udf(returnType=StringType())
    def geohash_4_udf(lat, lng):
        if lat is None or lng is None:
            return None
        try:
            return pygeohash.encode(lat, lng, precision=4)
        except Exception:
            return None
        
    def join_hotels_with_weather_by_geohash(self, hotels_df: DataFrame, weather_df: DataFrame) -> DataFrame:
        weather_df_clean = weather_df\
            .dropDuplicates(["geohash"])\
            .drop("lat", "lng")

        joined_df = hotels_df.join(
            weather_df_clean,
            on="geohash",
            how="left"
        )

        return joined_df