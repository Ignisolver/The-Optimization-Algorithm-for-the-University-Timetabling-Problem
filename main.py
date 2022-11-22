# todo data input - db API
# todo test db_api
from time import sleep

# todo optimize goal function weights
# todo tests

from algorithm.algorithm_ import algorithm
from algorithm.preprocessing import preprocess_all
from algorithm.summarizer import summarize_before, summarize_after
from data_generation.generator import generate_all
from data_presentation.data_presentation import generate_pdfs


def main():
    # Generacja danych
    all_ = generate_all()
    # Preprocessing danych
    summarize_before(all_)
    sorted_classes = preprocess_all(all_)
    # Działanie algorytmu
    alg_result = algorithm(sorted_classes)
    summarize_after(all_, alg_result)
    sleep(0.1)
    # Prezentacja wyników
    generate_pdfs(all_.groups, all_.lecturers, all_.rooms, all_.name)


if __name__ == "__main__":
    main()