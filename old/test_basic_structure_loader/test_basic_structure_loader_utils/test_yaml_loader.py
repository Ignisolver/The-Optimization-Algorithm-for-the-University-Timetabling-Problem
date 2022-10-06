from pathlib import Path

import pytest

from old.data_input.basic_structure_loader.basic_structure_loader_utils.yaml_loader import \
    YamlLoader


@pytest.fixture
def yl() -> YamlLoader:
    return YamlLoader()

@pytest.fixture
def file_path() -> Path:
    abs_path = Path(__file__).absolute()
    file_path = abs_path.parent.joinpath('data/test_data.yaml')
    return file_path


expected_yaml_str = """INT: 2
STR: "ola"
LIST:
  - 1
  - 2
  - 3
NONE: null"""

expected_data = {"INT": 2, "STR": "ola", "LIST":[1,2,3],"NONE": None}

class TestYamlLoader:
    def test__get_yaml_str_from_file__ok(self, yl, file_path):
        yaml_str = yl._get_yaml_str_from_file(file_path)
        assert yaml_str == expected_yaml_str

    def test__get_yaml_str_from_file__incorrect_path(self, yl):
        path = Path(r"C\iuyduvgjhbkniubh")
        with pytest.raises(FileNotFoundError):
            _ = yl._get_yaml_str_from_file(path)

    def test__load_data_from_yaml_string(self, yl):
        data = yl._load_data_from_yaml_string(expected_yaml_str)
        assert data == expected_data

    def test_load_data_from_yaml_file(self, yl, file_path):
        data = yl.load_data_from_yaml_file(file_path)
        assert data == expected_data
