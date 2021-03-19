# Daniel Kotlinski Sprint 4 Testing
# 3/18/21


import project1


def test_get_data():
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
                "id,school.city,school.state,school.name,2018.student.size,2017.student.size," \
                "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line," \
                f"2016.repayment.3_yr_repayment.overall"
    answer = project1.get_data(url)
    assert len(answer) > 1000


def test_web_to_database():
    values = [{"id": 283, "school.name": "Bridgewater State University", "school.state": "MA",
                "school.city": "Bridgewater",
                "2018.student.size": 20000, "2017.student.size": 19000,
                "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line": 1324,
                "2016.repayment.3_yr_repayment.overall": 82, "2016.repayment.repayment_cohort.3_year_declining_balance": 0.34}]
    checkvalues = [(283, "Bridgewater State University", "MA", "Bridgewater", 20000, 19000, 1324, 82, 0.34)]
    conn, cursor = project1.open_db("project_test_db.sqlite")
    cursor.execute('DROP TABLE IF EXISTS University_Info')
    project1.create_university_info(cursor)
    project1.web_to_database(cursor, values)
    sql = "SELECT * FROM University_Info"
    results = cursor.execute(sql).fetchall()
    assert results == checkvalues
    project1.close_db(conn)


def test_create_unemployment_data():
    excel_data_path = "state_M2019_dl.xlsx"
    conn, cursor = project1.open_db("project_db.sqlite")
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    project1.create_employment_data(cursor)
    project1.excel_to_database(excel_data_path, cursor)
    sqlTestQuery = "SELECT DISTINCT state FROM Employment_Data"
    results = cursor.execute(sqlTestQuery).fetchall()
    assert len(results) >= 50
    project1.close_db(conn)


def test_excel_to_database():
    excel_data_path = "test_file.xlsx"
    conn, cursor = project1.open_db("project_test_db")
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    project1.create_employment_data(cursor)
    project1.excel_to_database(excel_data_path, cursor)
    sqlTestQuery = "SELECT * FROM Employment_Data where o_group = 'major'"
    results = cursor.execute(sqlTestQuery).fetchall()
    assert len(results) == 9
    project1.close_db(conn)


def test_create_employment_data_table():
    conn, cursor = project1.open_db("project_test_db")
    sqlTest = "SELECT * FROM Employment_Data"
    results = cursor.execute(sqlTest).fetchall()
    assert len(results) == 9
    project1.close_db(conn)


def test_excel_to_database_exists():
    excel_data_path = "test_file.xlsx"
    conn, cursor = project1.open_db("project_test_db")
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    project1.create_employment_data(cursor)
    project1.excel_to_database(excel_data_path, cursor)
    sql = "SELECT * FROM Employment_Data"
    results = cursor.execute(sql).fetchall()
    assert len(results) == 9
    project1.close_db(conn)

