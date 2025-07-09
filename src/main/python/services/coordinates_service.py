from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, udf, expr
from pyspark.sql.types import StructType, StructField, DoubleType
from .geocoding_service import get_coordinates

class CoordinatesService:
    
    def __init__(self):
        pass
    
    def fill_null_lat_lng(self, df: DataFrame) -> DataFrame:
        df = df.withColumn("coordinates", when(
            col("lng").isNull() | col("lng").isNull(),
            self.get_coordinates_from_geocode_api(col("address"))
        ).otherwise(None))

        df = df.withColumn("lat", when(
            col("lat").isNull(),
            expr("try_cast(coordinates.lat as double)"))
            .otherwise(col("lat")))
        
        df = df.withColumn("lng", when(
            col("lng").isNull(),
            expr("try_cast(coordinates.lng as double)"))
            .otherwise(col("lng")))
        
        df = df.drop("coordinates")

        return df

    @staticmethod
    @udf(returnType=StructType([
        StructField("lat", DoubleType()),
        StructField("lng", DoubleType())
    ]))
    def get_coordinates_from_geocode_api(address):
        coords = get_coordinates(address)
        if coords:
             return {"lat": coords.get("lat"), "lng": coords.get("lng")}
        return None
