# Daniel Kotlinski Sprint 2 Tests
# 2/17/21


import main

# 1 assure that we get more than 1000 data items


def test_get_data():
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
                "id,school.city,school.name,2018.student.size,2017.student.size," \
                "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line," \
                "2016.repayment.3_yr_repayment.overall"
    answer = main.get_data(url)
    assert len(answer) > 1000

# 2 create new empty database, run table creation function, save data to the database then
# check to see the database contains test university


def test_insert_to_database():
    # create test dictionary data
    values = [{"id": 283, "school.name": "Bridgewater State University", "school.city": "Bridgewater",
              "2018.student.size": 20000, "2017.student.size": 19000,
              "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line": 1324,
              "2016.repayment.3_yr_repayment.overall": 82}]
    # checkvalues is just an array list of the values given, used to check if 'values' were inserted correctly
    checkvalues = [(283, "Bridgewater State University", "Bridgewater", 20000, 19000, 1324,82)]
    # creating a test database
    conn, cursor = main.open_db("project_test_db.sqlite")
    # drop the table so there are no primary key collisions if table already exists
    cursor.execute('DROP TABLE IF EXISTS University_Info')
    main.setup_db(cursor)
    main.insert_to_database(cursor, values)
    # sql query to get ALL data and compare
    sql = "SELECT * FROM University_Info"
    results = cursor.execute(sql).fetchall()
    assert results == checkvalues
    main.close_db(conn)
