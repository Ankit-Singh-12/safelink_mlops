from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        
        dataingestionconfig=DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        data_ingestion=DataIngestion(data_ingestion_config=dataingestionconfig)
        
        logging.info("Initiating the data ingestion process")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation process completed")
        print(dataingestionartifact)
        
        datavalidationconfig=DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,
                                       data_validation_config=datavalidationconfig)
        
        logging.info("Initiating the data validation process")
        datavalidationartifact=data_validation.initiate_data_validation()
        logging.info("Data validation process completed")
        print(datavalidationartifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)