from safelink.components.data_ingestion import DataIngestion
from safelink.components.data_validation import DataValidation
from safelink.components.data_transformation import DataTransformation
from safelink.components.model_trainer import ModelTrainer
from safelink.exception.exception import SafeLinkException
from safelink.logging.logger import logging
from safelink.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
from safelink.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        
        #--------------------------------Data Ingestion---------------------------------
        dataingestionconfig=DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        data_ingestion=DataIngestion(data_ingestion_config=dataingestionconfig)
        
        logging.info("Initiating the data ingestion process")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation process completed")
        print(f"Data Ingestion Artifact: {dataingestionartifact}")
        
        #--------------------------------Data Validation---------------------------------
        datavalidationconfig=DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,
                                       data_validation_config=datavalidationconfig)
        
        logging.info("Initiating the data validation process")
        datavalidationartifact=data_validation.initiate_data_validation()
        logging.info("Data validation process completed")
        print(f"Data Validation Artifact: {datavalidationartifact}")
        
        #--------------------------------Data Transformation---------------------------------
        datatransformationconfig=DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact=datavalidationartifact,
                                               data_transformation_config=datatransformationconfig)
        
        logging.info("Initiating the data transformation process")
        datatransformationartifact=data_transformation.initiate_data_transformation()
        logging.info("Data transformation process completed")
        print(f"Data Transformation Artifact: {datatransformationartifact}")
        
        #-------------------------------Model Trainer---------------------------------
        modeltrainerconfig=ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=modeltrainerconfig,
                                    data_transformation_artifact=datatransformationartifact)
        
        logging.info("Initiating the model trainer process")
        modeltrainerartifact=model_trainer.initiate_model_trainer()
        logging.info("Model trainer process completed")
        print(f"Model Trainer Artifact: {modeltrainerartifact}")
    

    except Exception as e:
        raise SafeLinkException(e,sys)