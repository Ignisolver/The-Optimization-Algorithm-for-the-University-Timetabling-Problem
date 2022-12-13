# todo data input - db API
# todo test db_api
from time import sleep


from algorithm.algorithm_ import algorithm
from algorithm.summarizer import summarize_before, summarize_after
from algorithm.preprocessing import preprocess_all
from data_generation.generator import generate_all
from data_presentation.data_presentation import generate_pdfs
from utils.res_saver import dump
from utils.test_result import TestResult
from utils.utils_ import turn_off_print


def main():
    # Generacja danych
    all_ = generate_all()
    # Preprocessing danych
    b_res = summarize_before(all_)
    sorted_classes = preprocess_all(all_)
    # Działanie algorytmu
    alg_result = algorithm(sorted_classes)
    aft_res = summarize_after(all_, alg_result)
    sleep(0.1)
    # Prezentacja wyników
    generate_pdfs(all_.groups, all_.lecturers, all_.rooms, all_.name)
    dump(TestResult(b_res, aft_res, alg_result))


if __name__ == "__main__":
    # turn_off_print()
    main()