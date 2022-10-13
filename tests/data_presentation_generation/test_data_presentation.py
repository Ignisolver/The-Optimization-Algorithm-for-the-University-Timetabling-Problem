import os
from pathlib import Path

from data_presentation.data_presentation import _save_yaml, _delete_yaml, \
    _save_pdf


def test_generate_pdfs():
    assert False


def test_generate_pdfs_for_items():
    assert False


def test_save_delete_yaml():
    f_name = "temp_test"
    folder_path = os.curdir
    file_path = Path(folder_path).joinpath(f"{f_name}.yaml")
    if f"{f_name}.yaml" in os.listdir(folder_path):
        os.remove(file_path)

    _save_yaml(file_path, "KOZA: 1")
    assert f"{f_name}.yaml" in os.listdir(folder_path)
    _delete_yaml(file_path)
    assert f"{f_name}.yaml" not in os.listdir(folder_path)


def test_save_pdf():
    f_name = "temp_test"
    folder_path = os.curdir
    file_path = Path(folder_path).joinpath(f"{f_name}.yaml")
    yaml_txt = """- name: Work to live\n  days: MTWRF\n  time: 9-17"""
    _save_yaml(file_path, yaml_txt)
    _save_pdf(file_path)
    assert f"{f_name}.pdf" in os.listdir(folder_path)
    os.remove(file_path.with_suffix(".pdf"))
    _delete_yaml(file_path)
