# The Optimization Algorithm for the University Timetabling Problem

Date: 2022
## Description
this repository contains object-oriented implementation of optimization algorithm for creating a timetable for university. Algorithm was developd by myself. Until year 2022 it is my the biggest python project made 100% by myself. An engineering thesis was created on the basis of this project. Prjoect is covered with 145 unittests.

Algorithm assigns time and room for the classes. Lecturer and groups are asigned for the classes in advance. Algorithm tries to create timetables for all groups, lecturers and groups. It also optimizes:
- brake time between classes
- classes time
- load uniformity
- amount of free days

Implementation consists of:
- data types
- data generation
- data presentation
- algorithm implementation
- USOS scraper
- unittests
- algorithm test cases

## main
Contains main() function which generates data according to configuration, run the algorithm, generate pdf-s with schedules, and represent results.

## MAIN_TESTS
Some specific tests of algorithm.

## algorithm
Package contains implementation of inter alia:
- algorithm
- goal function
- summarising module

## basic_structures
Object oriented model of data

## data_generation
Module for generateing data to test the algorithm

## data_presentation
Data presentation module. Represent algorithm results - loading bar and timetables in .pdf

## schedule
Implementation of day and week timetable data structure

## test
Unit test for most of written code

## time
Implementation module to manage time, time deltas and time ranges

## usos_scrapper
Module for scrap https://www.usos.agh.edu.pl/ webpages and download real data for tests

## utils
Some usefull tools

## RESULTS
### Time complexity
![obraz](https://user-images.githubusercontent.com/62255841/212315199-b76d3a53-d704-42ef-8471-b039efd25cba.png)
### Block diagram
![obraz](https://user-images.githubusercontent.com/62255841/212315350-c671b625-3ba0-4370-a796-4df9b032e42f.png)
### Algorithm during calculating
![obraz](https://user-images.githubusercontent.com/62255841/212315625-c6e67aba-7aae-4c9c-abf0-82d81207b278.png)
### Created timetables - examples
![obraz](https://user-images.githubusercontent.com/62255841/212315747-fab72069-dddb-4ebc-a13b-7e89fc95fa6f.png)
![obraz](https://user-images.githubusercontent.com/62255841/212315780-a85f4152-e865-4398-8ef2-71e823392e33.png)
![obraz](https://user-images.githubusercontent.com/62255841/212316677-db30635d-8bd0-4743-a8d6-d34cf602be69.png)
![obraz](https://user-images.githubusercontent.com/62255841/212316776-07cdfa1d-153c-422b-a069-a233d62fa43c.png)




