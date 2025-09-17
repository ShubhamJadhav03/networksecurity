import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR
import sys




class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()   # enable this if S3 sync is implemented

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Ingestion...")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed: {artifact}")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Validation...")
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
            )
            artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed: {artifact}")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Data Transformation...")
            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transformation_config
            )
            artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation completed: {artifact}")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    ## local Artifact will go to s3 Bucket
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    ## Local Final model will go to s3 Bucket
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)




    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting Model Training...")
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=model_trainer_config,
            )
            artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training completed: {artifact}")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            ingestion_artifact = self.start_data_ingestion()
            validation_artifact = self.start_data_validation(data_ingestion_artifact=ingestion_artifact)
            transformation_artifact = self.start_data_transformation(data_validation_artifact=validation_artifact)
            model_artifact = self.start_model_trainer(data_transformation_artifact=transformation_artifact)

            # Sync model artifact to S3
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

            return model_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
