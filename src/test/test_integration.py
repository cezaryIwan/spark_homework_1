import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)
src_main_python = os.path.join(project_root, "src", "main", "python")
sys.path.insert(0, src_main_python)

import shutil
import pytest
from pyspark.sql import SparkSession
from src.main.python.main import run_etl_pipeline

'''
Integration test for debugging purposes.
'''

@pytest.fixture(scope="module")
def spark():
    spark_session = SparkSession.builder \
        .master("local[*]") \
        .appName("ETL Test") \
        .getOrCreate()
    yield spark_session
    spark_session.stop()

@pytest.fixture(scope="module")
def test_data_dir(tmp_path_factory, spark):
    temp_dir = tmp_path_factory.mktemp("test_data")

    test_dir = os.path.abspath(os.path.dirname(__file__))
    input_dir = os.path.join(test_dir, "resources")
    hotels_csv = os.path.join(input_dir, "test_data_hotel_full.csv")
    weather_csv = os.path.join(input_dir, "test_data_weather_full.csv")

    hotels_target = os.path.join(temp_dir, "hotels.csv")
    shutil.copy(hotels_csv, hotels_target)

    df_weather = spark.read.option("header", True).csv(weather_csv)
    weather_parquet_path = os.path.join(temp_dir, "weather.parquet")
    df_weather.write.mode("overwrite").parquet(weather_parquet_path)

    return {
        "hotels_path": hotels_target,
        "weather_path": weather_parquet_path
    }

def test_run_etl_pipeline(spark, test_data_dir):
    df_result = run_etl_pipeline(
        spark,
        hotels_path=test_data_dir["hotels_path"],
        weather_path=test_data_dir["weather_path"]
    )
    result_dicts = [row.asDict() for row in df_result.collect()]