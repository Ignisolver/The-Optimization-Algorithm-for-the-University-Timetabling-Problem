from pathlib import Path

from yaml import safe_load


class YamlLoader:
    @staticmethod
    def _get_yaml_str_from_file(abs_file_path: Path) -> str:
        with open(abs_file_path, 'r') as file:
            lines = file.readlines()
        text = "".join(lines)
        return text

    @staticmethod
    def _load_data_from_yaml_string(yaml_str: str) -> dict:
        return safe_load(yaml_str)

    def load_data_from_yaml_file(self, file_path: Path):
        yaml_str = self._get_yaml_str_from_file(file_path)
        return self._load_data_from_yaml_string(yaml_str)
