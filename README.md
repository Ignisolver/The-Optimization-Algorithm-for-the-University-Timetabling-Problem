# The Optimization Algorithm for the University Timetabling Problem

Date: 2022
## Description
this repository contains object-oriented implementation of optimization algorithm for creating a timetable for university. Algorithm was developd by myself. Until year 2022 it is my the biggest python project made 100% by myself. An engineering thesis was created on the basis of this project. Prjoect is covered with 145 unittests.

Implementation consists of:
- datatypes
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

