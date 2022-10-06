from yaml import safe_load

from time_ import Time
from utils.constans import root_path
with open(root_path.joinpath("data/configuration.yaml"), 'r') as file:
    configuration: dict = safe_load(file)

MAX_HOUR = Time(configuration["MAX_HOUR"]["HOUR"],
                configuration["MAX_HOUR"]["MINUTE"])

MIN_HOUR = Time(configuration["MIN_HOUR"]["HOUR"],
                configuration["MIN_HOUR"]["MINUTE"])
