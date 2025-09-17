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

# Uncomment only if you are using S3 syncing
# from networksecurity.cloud_storage.s3_syncer import S3Sync
# from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME, SAVED_MODEL_DIR


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        # self.s3_sync = S3Sync()   # enable this if S3 sync is implemented

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

            # Optional: sync model to S3
            # self.s3_sync.sync_folder_to_s3(
            #     folder=os.path.join("final_model"),
            #     bucket_name=TRAINING_BUCKET_NAME,
            #     bucket_folder=SAVED_MODEL_DIR,
            # )

            return model_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
