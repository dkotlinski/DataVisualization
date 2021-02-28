# Daniel Kotlinski Sprint 3 read data out of an excel file to add to database
# 2/23/21


import openpyxl
import requests
import secrets
import sqlite3
from typing import Tuple


def get_data(url: str):
    # takes in our url and adds needed info
    # uses get_meta to grab total number of iterations needed
    # loops through 'results' data, adds it to an array, and returns the array
    final_data = []
    numpage = get_meta(url)
    for i in range(numpage):
        final_url = f"{url}&api_key={secrets.api_key}&page={i}"
        response = requests.get(final_url)
        json_data = response.json()
        page_data = json_data["results"]
        if response.status_code != 200:
            print(response.text)
            return final_data
        else:
            final_data.extend(page_data)
    return final_data


def get_meta(url: str):
    # takes in our base url at page 0
    # use metadata to find how many pages of data there are
    furl = f"{url}&api_key={secrets.api_key}&page=0"
    response = requests.get(furl)
    json_data = response.json()
    meta_data = json_data["metadata"]
    total_data = meta_data.get("total")
    pages = meta_data.get("per_page")
    pagenum = (round(total_data/pages)+1)
    return pagenum


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def create_university_info(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS University_Info(
    id INTEGER PRIMARY KEY,
    school_name TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT NULL,
    student_size_2017 INTEGER DEFAULT NULL,
    earnings_2017 INTEGER DEFAULT NULL,
    repayment_2016 INTEGER DEFAULT NULL
    );''')


def create_employment_data(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employment_Data (
    occ_code TEXT NOT NULL,
    area INTEGER NOT NULL,
    state TEXT NOT NULL,
    occupation_major_title TEXT NOT NULL,
    totalemployment_perfield_perstate INTEGER,
    hourly_25th_percentile FLOAT DEFAULT NULL,
    annual_25th_percentile INTEGER DEFAULT NULL,
    o_group TEXT NOT NULL,
    PRIMARY KEY(occ_code, state, occupation_major_title)
    )''')


def web_to_database(cursor: sqlite3.Cursor, all_data):
    for data in all_data:
        cursor.execute('''INSERT INTO University_Info(id, school_name, school_city, student_size_2018
                , student_size_2017, earnings_2017, repayment_2016)
                VALUES (?,?,?,?,?,?,?)''', (data["id"], data["school.name"], data["school.city"],
                                            data["2018.student.size"],
                                            data["2017.student.size"],
                                            data["2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line"],
                                            data["2016.repayment.3_yr_repayment.overall"]))


def excel_to_database(excel_data, cursor: sqlite3.Cursor):
    # load workbook .xlsx file
    workbook_file = openpyxl.load_workbook(excel_data)
    worksheet = workbook_file.active
    # iterate through all data in every row
    for data in worksheet.rows:
        # make sure we only take the major o_groups into our DB
        o_group = data[9].value
        if o_group == "major":
            # designate column names given data
            area = data[0].value
            state = data[1].value
            major_title = data[8].value
            totalemployment_perfield_perstate = data[10].value
            hourly_25th_percentile = data[19].value
            annual_25th_percentile = data[24].value
            occupational_code = data[7].value
            cursor.execute('''INSERT INTO Employment_Data (occ_code, area, state, occupation_major_title
                    , totalemployment_perfield_perstate, hourly_25th_percentile, annual_25th_percentile, o_group)
                    VALUES (?,?,?,?,?,?,?,?)''', (occupational_code, area, state,
                                                major_title,
                                                totalemployment_perfield_perstate,
                                                hourly_25th_percentile,
                                                annual_25th_percentile, o_group))


def main():
    # main function to hold base URL and call other functions
    # open and read the given excel file, print contents to console
    excel_data = "state_M2019_dl.xlsx"
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
          "id,school.city,school.name,2018.student.size,2017.student.size," \
          "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    # enter url into function to grab data
    all_data = get_data(url)
    # now put data into a database
    conn, cursor = open_db("project_db.sqlite")
    # drop existing table so there are no primary key errors
    cursor.execute('DROP TABLE IF EXISTS University_Info')
    # create database for university info
    create_university_info(cursor)
    # drop existing table so there are no primary key errors
    cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    # create database for employment data
    create_employment_data(cursor)
    # insert data into databases
    excel_to_database(excel_data, cursor)
    web_to_database(cursor, all_data)
    close_db(conn)


if __name__ == '__main__':
    main()
