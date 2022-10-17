import os
import shutil
from pathlib import Path

import pytest

from basic_structures import Room
from basic_structures.classes import UnavailableClasses
from data_presentation.data_presentation import _save_yaml, _delete_yaml, \
    _save_pdf, _generate_pdfs_for_items, generate_pdfs
from time_ import Time, TimeDelta
from utils.constans import ROOT_PATH
from utils.types_ import MONDAY


@pytest.fixture
def items():
    un_av_cl = UnavailableClasses(day=MONDAY, start=Time(10, 20),
                                  dur=TimeDelta(1,1))
    rooms = [Room(1,12,12,"R1"),
             Room(2,12,12,"R2"),
             Room(3,12,12,"R3"),
             Room(4,12,12,"R4"),
             Room(5,12,12,"R5"),
             Room(6,12,12,"R6")]
    for i in range(len(rooms)):
        rooms[i].assign(un_av_cl)
    return rooms


def test_generate_pdfs(items):
    generate_pdfs(items, items, items, "unit_tests")
    path = ROOT_PATH.joinpath("results").joinpath("unit_tests")
    names = ("groups", "lecturers", "rooms")
    assert all(elem in os.listdir(path) for elem in names)
    assert len(os.listdir(path.joinpath("rooms"))) == 6
    shutil.rmtree(path)


def test_generate_pdfs_for_items(items):
    path = Path(__file__).parent
    name = "rooms"
    _generate_pdfs_for_items(path, name, items)
    assert name in os.listdir(path)
    folder_path = path.joinpath("rooms")
    assert len(os.listdir(folder_path)) == len(items)
    shutil.rmtree(folder_path)


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
