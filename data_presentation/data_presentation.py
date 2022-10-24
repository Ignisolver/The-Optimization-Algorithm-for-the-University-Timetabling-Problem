import os
from os import system
from pathlib import Path
from typing import List

from basic_structures.with_schedule import WithSchedule
from utils.constans import ROOT_PATH


def generate_pdfs(groups, lecturers, rooms, name):
    result_path = ROOT_PATH.joinpath("results").joinpath(name)
    os.mkdir(result_path)
    names_items = (("groups", groups),
                   ("lecturers", lecturers),
                   ("rooms", rooms))
    for name, items in names_items:
        _generate_pdfs_for_items(result_path, name, items)


def _generate_pdfs_for_items(path: Path, name, items: List[WithSchedule]):
    folder_path = path.joinpath(name)
    os.mkdir(folder_path)
    for item in items:
        name = item.name
        file_path = folder_path.joinpath(name)
        yaml_txt = item.week_schedule.to_yaml()
        _save_yaml(file_path, yaml_txt)
        _save_pdf(file_path)
        _delete_yaml(file_path)


def _save_yaml(path: Path, text):
    path = path.with_suffix(".yaml")
    with open(path, 'w') as file:
        file.write(text)


def _save_pdf(path: Path):
    yaml_path = path.with_suffix(".yaml")
    pdf_path = path.with_suffix(".pdf")
    system(f'py -3.10 -m pdfschedule "{yaml_path}" "{pdf_path}"')


def _delete_yaml(path):
    yaml_path = path.with_suffix(".yaml")
    os.remove(yaml_path)