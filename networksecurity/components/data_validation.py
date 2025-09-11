from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, 
                 data_validation_config: DataValidationConfig):
        try:
           self.data_ingestion_artifact = data_ingestion_artifact
           self.data_validation_config = data_validation_config
           self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)   

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            num_of_cols = len(self.schema_config['columns'])
            logging.info(f"Required number of Columns: {num_of_cols}")
            logging.info(f"DataFrame has Columns: {dataframe.columns}")
            if len(dataframe.columns) == num_of_cols:
                logging.info("✅ Number of columns validation passed.")
                return True
            logging.error("❌ Number of columns validation failed.")
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def is_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            if 'numerical_columns' not in self.schema_config:
                logging.error("'numerical_columns' key not found in schema_config.")
                raise NetworkSecurityException("'numerical_columns' key missing in schema_config.", sys)
            required = set(self.schema_config['numerical_columns'])
            present = set(dataframe.select_dtypes(include=[np.number]).columns)

            missing = required - present

            if missing:
                logging.error(f"❌ Missing Numerical Columns: {missing}")
                return False

            logging.info("✅ Numerical columns validation passed.")
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.select_dtypes(include=[np.number]).columns:
                d1 = base_df[column].dropna()
                d2 = current_df[column].dropna()
                is_same_dist = ks_2samp(d1, d2)

                if threshold <= is_same_dist.pvalue:
                    is_found = False  # No drift
                else:
                    is_found = True   # Drift detected
                    status = False

                report[column] = {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            if status:
                logging.info("✅ No data drift detected between train and test.")
            else:
                logging.warning("⚠️ Data drift detected. Check drift report for details.")

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate Number of Columns    
            if not self.validate_number_of_columns(train_dataframe):
                raise NetworkSecurityException("Train DataFrame does not contain all required columns.", sys)

            if not self.validate_number_of_columns(test_dataframe):
                raise NetworkSecurityException("Test DataFrame does not contain all required columns.", sys)

            # Validate Numerical Columns
            if not self.is_numerical_columns_exist(train_dataframe):
                raise NetworkSecurityException("Train DataFrame missing required numerical columns.", sys)

            if not self.is_numerical_columns_exist(test_dataframe):
                raise NetworkSecurityException("Test DataFrame missing required numerical columns.", sys)

            logging.info("✅ Schema validation checks passed for both train and test DataFrames.")

            # Check Data Drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            logging.info("✅ Validated train and test DataFrames saved successfully.")

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info("✅ Data Validation Artifact created successfully.")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
