from pyspark.sql.functions import expr
from pyspark.sql import DataFrame
from app_config import app_config

class EncryptionService:
    def __init__(self):
        pass
    
    def pii_fields(self) -> list[str]:
        return [
            'full_name', 'home_address', 'email_address', 'phone_number',
            'national_id_numbers', 'passport_number', 'driver’s_license_number',
            'tax_identification_number', 'face_photos', 'fingerprints', 'retinal_scans',
            'ip_address', 'date_of_birth', 'place_of_birth', 'gender', 'race',
            'job_title', 'employer', 'education_history', 'geolocation_data',
            'login_usernames', 'device_ids', 'mac_addresses', 'browsing_behavior',
            'name', 'address', 'phone', 'email'
        ]
    
    @staticmethod
    def encrypt_fields(df: DataFrame, fields: list[str]) -> DataFrame:
        key = app_config['AES_ENCRYPTION_KEY'] 
        fields_to_encrypt = [f for f in fields if f in df.columns]
        for field in fields_to_encrypt:
            df = df.withColumn(
                field,
                expr(f"aes_encrypt(cast({field} as binary), unhex('{key}'))")
            )
        return df
