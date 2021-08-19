# Daniel Kotlinski Data Visualization
# 3/14/2021

The goal of this project was to create a state-by-state comparison of the number of college graduates to the number of jobs likely to require a college degree, as well as compare the annual loan repayment to the 25th percentile salary. Using JSON APIs, this Python-based program retrieves 3,200 rows of data from the College Scorecard website (https://collegescorecard.ed.gov/data) to populate a table in a SQLite database. The program then retrieves 36,600+ rows of data from the 2019 Occupational Employment Statistics Excel file to populate a new table in the same database. The program then uses Plotly to create a choropleth map to vi- sualize the resulting data. This project includes automated tests in Python, GitHub actions, and some YML. 
The following metadata is collected:
id, school.name, school.city, 2018.student.size, 2017.student.size, 2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,
2016.repayment.3_yr_repayment.overall, **2016.repayment.repayment_cohort.3_year_declining_balance** from universities with degrees of type 2 and 3 using gov api key with python. 

A sqlite database is created and populated with all 3203 school's data. Data is then displayed as a visualization choropleth map.

**New in sprint 4**, We now disregard OCC codes 30-49, and add a new row to our database table - the 2016 loan repayment.
The program also displays data via two choropleth maps using plotly.



