# DanielKotlinski_Sprint3
# 3/14/2021

**IMPORTANT info for test_project1.py:**
GUI buttons are a bit __wonky__. The functions that display the maps can be run separately in the main function (they are
currently commented out). Had some trouble getting the GUI to work, never had to code one before so it was a large learning
process. Git commits/pushes/comments are a bit sparse... This is because I was fooling around so much to get my GUI working,
that I did not want to destroy **your email** or mine with failed pytests.

This is **Sprint 4** of project 1. This program retrieves: 

id, school.name, school.city, 2018.student.size, 2017.student.size, 2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,
2016.repayment.3_yr_repayment.overall, **2016.repayment.repayment_cohort.3_year_declining_balance** from universities with degrees of type 2 and 3 using gov api key
and python. A sqlite database is created and populated with all 3203 school's data. Data is then displayed either via text OR
as a visualization choropleth map.

**New in sprint 4**, We now disregard OCC codes 30-49, and add a new row to our database table - the 2016 loan repayment.
The program also displays data via text OR two choropleth maps using plotly.


**Tests**
Tests for sprints 2 and 3 are updated with the new requirements so that everything should work.
As stated, GUI was very wonky and running low on time trying to get those major components to work so there are
no tests for sprint 4. I just wanted to get the GUI working and update the old tests so that they would still work.

