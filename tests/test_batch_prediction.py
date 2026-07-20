import os
import pickle

import numpy as np
import pandas as pd

from safelink.pipeline.batch_prediction import BatchPrediction, PREDICTED_COLUMN


class _FakePreprocessor:
    def transform(self, x):
        return np.asarray(x)


class _FakeModel:
    def predict(self, x):
        # Predict 1 if row sum > 0 else 0
        return (np.asarray(x).sum(axis=1) > 0).astype(int)


def _dump(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def test_batch_prediction_adds_column_and_writes_output(tmp_path):
    preprocessor_path = os.path.join(tmp_path, "preprocessor.pkl")
    model_path = os.path.join(tmp_path, "model.pkl")
    output_dir = os.path.join(tmp_path, "prediction_output")

    _dump(_FakePreprocessor(), preprocessor_path)
    _dump(_FakeModel(), model_path)

    df = pd.DataFrame({"f1": [1, -1, 2], "f2": [1, -2, 3]})

    batch = BatchPrediction(
        preprocessor_path=preprocessor_path,
        model_path=model_path,
        output_dir=output_dir,
        output_file_name="out.csv",
    )
    result = batch.predict(df)

    # Column added
    assert PREDICTED_COLUMN in result.columns
    assert list(result[PREDICTED_COLUMN]) == [1, 0, 1]

    # Output file written
    output_file = os.path.join(output_dir, "out.csv")
    assert os.path.exists(output_file)

    saved = pd.read_csv(output_file)
    assert PREDICTED_COLUMN in saved.columns
    assert len(saved) == len(df)