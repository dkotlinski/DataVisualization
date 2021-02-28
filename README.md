# DanielKotlinski_Sprint3
# 2/28/2021

**IMPORTANT info for test_main.py:**

The paths in tests for the Excel file are hardcoded. If given the Excel file name, an error occurs "file not found"
Important to note that this is not the case in main.py. 
Working on finding a solution for this, for now I suppose it is better you _enter your own path_...

This is **Sprint 3** of project 1. This program retrieves: 

id, school.name, school.city, 2018.student.size, 2017.student.size, 2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,
2016.repayment.3_yr_repayment.overall, from universities with degrees of type 2 and 3 using gov api key
and python. A sqlite database is created and populated with all 3203 school's data.

**New in sprint 3**, retrieves data from the Occupational Employment Statistics 2019 Excel file.
Taking in all data, it populates a new table in our database with major occupations ONLY.

**Specific to the code**
There are multiple lines inside of main() that drops table on start up. They are commented out but useful when running the program multiple times to avoid sql collision errors. 
ID is used as the primary key (assuming school names are not unique) in our school data table.
State, OCC Code, and Occupation Title are used as the primary key in our employment data table.

**Tests and workflow problems**
All automated tests for sprint 2 & 3 are included. Working on fixing workflow errors where it says that there are no tests found,
even though in pycharm
_there are, and they all work._

