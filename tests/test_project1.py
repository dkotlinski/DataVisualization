# Daniel Kotlinski Sprint 3 Tests
# 2/23/21


import project1
# Sprint 2
# 1 assure that we get more than 1000 data items


def test_get_data():
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
                "id,school.city,school.name,2018.student.size,2017.student.size," \
                "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line," \
                "2016.repayment.3_yr_repayment.overall"
    answer = project1.get_data(url)
    assert len(answer) > 1000

# 2 create new empty database, run table creation function, save data to the database then
# check to see the database contains test university


def test_web_to_database():
    # create test dictionary data
    values = [{"id": 283, "school.name": "Bridgewater State University", "school.city": "Bridgewater",
              "2018.student.size": 20000, "2017.student.size": 19000,
              "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line": 1324,
              "2016.repayment.3_yr_repayment.overall": 82}]
    # checkvalues is just an array list of the values given, used to check if 'values' were inserted correctly
    checkvalues = [(283, "Bridgewater State University", "Bridgewater", 20000, 19000, 1324,82)]
    # creating a test database
    conn, cursor = project1.open_db("project_test_db.sqlite")
    # drop the table so there are no primary key collisions if table already exists
    cursor.execute('DROP TABLE IF EXISTS University_Info')
    project1.create_university_info(cursor)
    project1.web_to_database(cursor, values)
    # sql query to get ALL data and compare
    sql = "SELECT * FROM University_Info"
    results = cursor.execute(sql).fetchall()
    assert results == checkvalues
    project1.close_db(conn)


# Sprint 3
# 1 make sure you get data from all 50 states from the original data
def test_create_unemployment_data():
    # hardcode path ONLY in test, without it we are told "file not found"
    excel_data_path = "state_M2019_dl.xlsx"
    conn, cursor = project1.open_db("project_db.sqlite")
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    project1.create_employment_data(cursor)
    project1.excel_to_database(excel_data_path, cursor)
    # after creating and opening the database, run sql query to check we have 50 states
    # this sql statement also includes 4 US territories
    sqlTestQuery = "SELECT DISTINCT state FROM Employment_Data"
    results = cursor.execute(sqlTestQuery).fetchall()
    assert len(results) >= 50
    project1.close_db(conn)

# 2 maybe create a test xlsx with a limited number of major occupational
#   groups along with some other stuff. make sure you get the right number of major occupational groups


def test_excel_to_database():
    # hardcode path ONLY in test, without it we are told "file not found"
    excel_data_path = "test_file.xlsx"
    # create/use project_test_db so we do not ruin our project_db
    # project_test_db has edited o_groups that say "major", this is for testing purposes since the test database
    # is only 50 rows, if o_groups were not replaced with "major", we would return 1 result.. which is not enough
    conn, cursor = project1.open_db("project_test_db")
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    project1.create_employment_data(cursor)
    project1.excel_to_database(excel_data_path, cursor)
    # after creating and opening the database, run sql query to check we have 50 states
    # this sql statement also includes 4 US territories
    sqlTestQuery = "SELECT * FROM Employment_Data where o_group = 'major'"
    results = cursor.execute(sqlTestQuery).fetchall()
    assert len(results) == 9
    project1.close_db(conn)

# 3 write a test to make sure the new table is there


def test_create_employment_data_table():
    # open project_test_db, not modifying anything or dropping
    conn, cursor = project1.open_db("project_test_db")
    # this small database has 9 rows, all major data (coming from our excel file of 50 rows of mixed major and detailed)
    # get all data from table
    sqlTest = "SELECT * FROM Employment_Data"
    results = cursor.execute(sqlTest).fetchall()
    assert len(results) == 9
    project1.close_db(conn)

# 4 write a test to make sure that your new write to table works


def test_excel_to_database_exists():
    # hardcode path ONLY in test, without it we are told "file not found"
    excel_data_path = "test_file.xlsx"
    # create/use project_test_db so we do not ruin our project_db
    conn, cursor = project1.open_db("project_test_db")
    # drop table so it no longer exists
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    # create table
    project1.create_employment_data(cursor)
    # write to  database from excel file with 50 total rows, 9 of which are major o_group
    project1.excel_to_database(excel_data_path, cursor)
    # get all 9 rows to compare using sql
    sql = "SELECT * FROM Employment_Data"
    results = cursor.execute(sql).fetchall()
    assert len(results) == 9
    project1.close_db(conn)
