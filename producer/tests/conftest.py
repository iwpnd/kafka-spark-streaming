import pytest


@pytest.fixture(scope="session")
def mock_data_file(tmpdir_factory):
    mock_data = """[{"test1":"test"},
    {"test2":"test"},
    {"test3":"test"}]
    """

    fn = tmpdir_factory.mktemp("data").join("mock_data.json")

    with open(fn, "w") as f:
        f.write(mock_data)

    return fn
