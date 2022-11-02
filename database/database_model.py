from sqlalchemy import (create_engine, Column, Integer,
                        String, ForeignKey, Time)
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class LecturersTab(Base):
    __tablename__ = "lecturers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ClassesTab(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    duration = Column(Integer, nullable=False)
    type = Column(String)
    lecturer_id = Column(Integer, ForeignKey(LecturersTab.id), nullable=False)


class BuildingTab(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class RoomsTab(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    building_id = Column(Integer, ForeignKey(BuildingTab.id), nullable=False)
    capacity = Column(Integer, nullable=False)


class ClassesAvailableRoomsTab(Base):
    __tablename__ = "classes_available_rooms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    classes_id = Column(Integer, ForeignKey(ClassesTab.id), nullable=False)
    room_id = Column(Integer, ForeignKey(RoomsTab.id), nullable=False)


class GroupsTab(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    amount_of_students = Column(Integer)


class ClassesGroupsTab(Base):
    __tablename__ = "classes_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    classes_id = Column(Integer, ForeignKey(ClassesTab.id), nullable=False)
    group_id = Column(Integer, ForeignKey(GroupsTab.id), nullable=False)


class RoomsUnavailableTimes(Base):
    __tablename__ = "rooms_unavailable_time"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey(RoomsTab.id), nullable=False)
    day_nr = Column(Integer)  # 1-7
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)


class LecturersUnavailableTimes(Base):
    __tablename__ = "lecturers_unavailable_time"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lecturer_id = Column(Integer, ForeignKey(LecturersTab.id), nullable=False)
    day_nr = Column(Integer)  # 1-7
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)


class DistancesTab(Base):
    __tablename__ = "distances"
    id = Column(Integer, primary_key=True, autoincrement=True)
    building_1 = Column(Integer, ForeignKey(BuildingTab.id))
    building_2 = Column(Integer, ForeignKey(BuildingTab.id))
    distance = Column(Integer)
