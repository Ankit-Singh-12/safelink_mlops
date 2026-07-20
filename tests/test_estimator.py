import numpy as np

from safelink.utils.ml_utils.model.estimator import SafeLinkModel


class _FakePreprocessor:
    def transform(self, x):
        # Simple deterministic transform: pass-through doubling
        return np.asarray(x) * 2


class _FakeModel:
    def predict(self, x):
        # Return sum of each row as the "prediction"
        return np.asarray(x).sum(axis=1)


def test_safelink_model_predict_applies_preprocessor_then_model():
    model = SafeLinkModel(preprocessor=_FakePreprocessor(), model=_FakeModel())

    x = np.array([[1, 2], [3, 4]])
    # transform doubles -> [[2,4],[6,8]] -> row sums -> [6, 14]
    result = model.predict(x)

    assert np.array_equal(result, np.array([6, 14]))


def test_safelink_model_stores_components():
    pre = _FakePreprocessor()
    mdl = _FakeModel()
    model = SafeLinkModel(preprocessor=pre, model=mdl)

    assert model.preprocessor is pre
    assert model.model is mdl