import os
import sys

import numpy as np
import pytest

from safelink.utils.main_utils.utils import (
    read_yaml_file,
    write_yaml_file,
    save_numpy_array_data,
    load_numpy_array_data,
    save_object,
    load_object,
)
from safelink.exception.exception import SafeLinkException


def test_write_and_read_yaml(tmp_path):
    file_path = os.path.join(tmp_path, "sub", "config.yaml")
    content = {"a": 1, "b": ["x", "y"], "c": {"nested": True}}

    write_yaml_file(file_path, content)
    assert os.path.exists(file_path)

    loaded = read_yaml_file(file_path)
    assert loaded == content


def test_write_yaml_replace_overwrites(tmp_path):
    file_path = os.path.join(tmp_path, "config.yaml")

    write_yaml_file(file_path, {"value": 1})
    write_yaml_file(file_path, {"value": 2}, replace=True)

    assert read_yaml_file(file_path) == {"value": 2}


def test_save_and_load_numpy_array(tmp_path):
    file_path = os.path.join(tmp_path, "arr.npy")
    array = np.array([[1, 2, 3], [4, 5, 6]])

    save_numpy_array_data(file_path, array)
    loaded = load_numpy_array_data(file_path)

    assert np.array_equal(array, loaded)


def test_save_and_load_object(tmp_path):
    file_path = os.path.join(tmp_path, "obj.pkl")
    obj = {"model": "safelink", "params": [1, 2, 3]}

    save_object(file_path, obj)
    loaded = load_object(file_path)

    assert loaded == obj


def test_load_object_missing_file_raises(tmp_path):
    missing = os.path.join(tmp_path, "does_not_exist.pkl")
    with pytest.raises(SafeLinkException):
        load_object(missing)


def test_read_yaml_missing_file_raises(tmp_path):
    missing = os.path.join(tmp_path, "missing.yaml")
    with pytest.raises(SafeLinkException):
        read_yaml_file(missing) 