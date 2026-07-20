import os
import sys

import pandas as pd

from safelink.exception.exception import SafeLinkException
from safelink.logging.logger import logging
from safelink.utils.main_utils.utils import load_object
from safelink.utils.ml_utils.model.estimator import SafeLinkModel
from safelink.constant.training_pipeline import (
    FINAL_PREPROCESSOR_FILE_PATH,
    FINAL_MODEL_FILE_PATH,
    PREDICTION_OUTPUT_DIR,
    PREDICTION_OUTPUT_FILE_NAME,
)

PREDICTED_COLUMN = "predicted_column"


class BatchPrediction:
    def __init__(
        self,
        preprocessor_path: str = FINAL_PREPROCESSOR_FILE_PATH,
        model_path: str = FINAL_MODEL_FILE_PATH,
        output_dir: str = PREDICTION_OUTPUT_DIR,
        output_file_name: str = PREDICTION_OUTPUT_FILE_NAME,
    ):
        try:
            self.preprocessor_path = preprocessor_path
            self.model_path = model_path
            self.output_dir = output_dir
            self.output_file_name = output_file_name
        except Exception as e:
            raise SafeLinkException(e, sys)

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            preprocessor = load_object(self.preprocessor_path)
            model = load_object(self.model_path)
            safe_link_model = SafeLinkModel(preprocessor=preprocessor, model=model)

            df[PREDICTED_COLUMN] = safe_link_model.predict(df)

            os.makedirs(self.output_dir, exist_ok=True)
            output_path = os.path.join(self.output_dir, self.output_file_name)
            df.to_csv(output_path, index=False)
            logging.info(f"Batch prediction completed. Output saved to {output_path}")

            return df
        except Exception as e:
            raise SafeLinkException(e, sys)