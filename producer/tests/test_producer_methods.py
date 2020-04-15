import types

from .helpers import utils
from producer.producer import methods


def test_lazy_load_json_generator(mock_data_file):
    test = methods.lazy_load_json(mock_data_file)
    assert isinstance(test, types.GeneratorType)


def test_lazy_load_json_valid(mock_data_file):
    record = methods.lazy_load_json(mock_data_file)
    object1 = next(record)
    assert object1["test1"]
    assert utils.is_json(object1)
    object2 = next(record)
    assert object2["test2"]
    assert utils.is_json(object2)
    object3 = next(record)
    assert object3["test3"]
    assert utils.is_json(object3)
