# DanielKotlinski_Sprint2
# 2/17/2021

This is sprint 2 of project 1. This program retrieves: 

id
school.name
school.city
2018.student.size
2017.student.size
2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line
2016.repayment.3_yr_repayment.overall

from universities with degrees of type 2 and 3 using gov api key and python.

A sqlite database is created and populated with all 3203 school's data.
There is a line inside of main() that drops table on start up. It is commented out but useful when running the program multiple times to avoid sql collision errors. 
Id is used as the primary key (assuming school names are not unique).
Also included are the proper 2 test cases, commented to state what they actually do.

