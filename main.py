# todo data input - db API
# todo test db_api

# todo testy na one week funkcji celu

# może mogło by być tak że maksymalna liczba zajęć w tygodniu jest ustalana na bierząco przy przypisywaniu??
# todo zmiany w funkcji celu
# todo jak jedne zajęcia są w dwóch porach dają więcej punktów!!!!
# todo summariser

from algorithm.algorithm_ import algorithm
from algorithm.preprocessing import assign_occupacity, get_sorted_classes, \
    add_info_to_week_schedule
from data_generation.generator import generate_all
from data_presentation.data_presentation import generate_pdfs


def main():
    # Generacja danych
    all_ = generate_all()
    classes = all_.classes
    # Preprocessing danych
    assign_occupacity(classes)
    add_info_to_week_schedule(classes)
    sorted_classes = get_sorted_classes(classes)
    # Działanie algorytmu
    algorithm(sorted_classes)
    # Prezentacja wyników
    generate_pdfs(all_.groups, all_.lecturers, all_.rooms, all_.name)

if __name__ == "__main__":
    main()