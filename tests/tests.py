# Daniel Kotlinski Sprint 2 Tests
# 2/17/21
# one test should the method that retrieves the data from the web and assure that you get more than 1000 data items
# The second test should create a new empty database, run your table creation function/method,
# then run your save data to database method then check to see that the database contains the test
# university that you just put there.

import main

# 1 assure that we get more than 1000 data items


def test_get_data():
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
                "id,school.city,school.name,2018.student.size,2017.student.size," \
                "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    answer = main.get_data(url)
    assert len(answer) > 1000

# 2 create new empty database, run table creation function, save data to the database then
# check to see the database contains test university

def test_insert_to_database():
    pass