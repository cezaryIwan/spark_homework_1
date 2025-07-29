import pytest
from pyspark.sql import SparkSession
from src.main.python.services.encryption_service import EncryptionService

@pytest.fixture(scope='module')
def spark():
    return SparkSession.builder \
        .master('local[1]') \
        .appName('PII Encryption Test') \
        .getOrCreate()

def test_encrypt_pii_fields(spark):
    csv_path = 'src/test/resources/test_data_hotel.csv'
    df = spark\
        .read.option('header', True).csv(csv_path)\
        .withColumnRenamed('Latitude', 'lat')\
        .withColumnRenamed('Longitude', 'lng')
        
    encryption_service = EncryptionService()

    encrypted_df = encryption_service.encrypt_fields(
        df,
        encryption_service.pii_fields()
    )

    for col in encryption_service.pii_fields():
        if col in df.columns:
            original_values = [row[col] for row in df.select(col).collect()]
            encrypted_values = [row[col] for row in encrypted_df.select(col).collect()]
            assert original_values != encrypted_values
            assert all(v is not None for v in encrypted_values)

    assert df.select('lat').collect() == encrypted_df.select('lat').collect()
    assert df.select('lng').collect() == encrypted_df.select('lng').collect()
