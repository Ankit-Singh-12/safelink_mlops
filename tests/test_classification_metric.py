import numpy as np

from safelink.utils.ml_utils.metric.classification_metric import get_classification_score
from safelink.entity.artifact_entity import ClassificationMetricArtifact


def test_get_classification_score_perfect_prediction():
    y_true = np.array([1, 0, 1, 0, 1])
    y_pred = np.array([1, 0, 1, 0, 1])

    metric = get_classification_score(y_true, y_pred)

    assert isinstance(metric, ClassificationMetricArtifact)
    assert metric.f1_score == 1.0
    assert metric.precision_score == 1.0
    assert metric.recall_score == 1.0


def test_get_classification_score_returns_floats_in_range():
    y_true = np.array([1, 0, 1, 1, 0, 1])
    y_pred = np.array([1, 0, 0, 1, 1, 1])

    metric = get_classification_score(y_true, y_pred)

    for value in (metric.f1_score, metric.precision_score, metric.recall_score):
        assert 0.0 <= value <= 1.0