# todo algorithm
# todo data input - db API
# todo test db_api
from algorithm.algorithm_ import algorithm
from algorithm.preprocessing import assign_occupacity, get_sorted_classes, \
    add_info_to_week_schedule
from data_generation.generator import generate_all


def main():
    all_ = generate_all()
    classes = all_.classes
    assign_occupacity(classes)
    add_info_to_week_schedule(classes)
    sorted_classes = get_sorted_classes(classes)
    algorithm(sorted_classes)
    print("FINISH!!!")


if __name__ == "__main__":
    main()