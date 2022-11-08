# todo data input - db API
# todo test db_api

# todo w planie ID zamiast nazwy
# todo dodanie minimalnego czasu przerwy???
# todo zmiany w funkcji celu
# todo testy na one week funkcji celu
# chyba jest nie tak w funkcji celu że podfunkcja dni wolnych sie zwiększa a nie zmniejsza
# może mogło by być tak że maksymalna liczba zajęć w tygodniu jest ustalana na bierząco przy przypisywaniu??
# jak jedne zajęcia są w dwóch porach dają więcej punktów

from algorithm.algorithm_ import algorithm
from algorithm.preprocessing import assign_occupacity, get_sorted_classes, \
    add_info_to_week_schedule
from data_generation.generator import generate_all
from data_presentation.data_presentation import generate_pdfs


def main():
    all_ = generate_all()
    classes = all_.classes
    assign_occupacity(classes)
    add_info_to_week_schedule(classes)
    sorted_classes = get_sorted_classes(classes)
    algorithm(sorted_classes)
    generate_pdfs(all_.groups, all_.lecturers, all_.rooms, all_.name)
    print("FINISH!!!")


if __name__ == "__main__":
    main()