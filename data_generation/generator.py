# set generation parameters
# buildings
# distances
# rooms
# times for rooms
# groups
# lecturers
# times for lecturers
# classes
# classes groups
# classes rooms

from generation_configs import *
from basic_structures.room import Building
buildings = [Building(i) for i in range(AMOUNT_OF_BUILDINGS)]



