# Daniel Kotlinski Sprint2 putting university data into a database
# 2/16/21


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
    db_connection = sqlite3.connect(filename)#connect to existing DB or create new one
    cursor = db_connection.cursor()#get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS University_Info(
    id INTEGER PRIMARY KEY,
    school_name TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT NULL,
    student_size_2017 INTEGER DEFAULT NULL,
    earnings_2017 INTEGER DEFAULT NULL,
    repayment_2016 INTEGER DEFAULT NULL
    );''')


def insert_to_database(cursor:sqlite3.Cursor, alldata):
    for data in alldata:
        cursor.execute('''INSERT INTO University_Info(id, school_name, school_city, student_size_2018
                , student_size_2017, earnings_2017, repayment_2016)
                VALUES (?,?,?,?,?,?,?)''', (data["id"], data["school.name"], data["school.city"], data["2018.student.size"],
                data["2017.student.size"], data["2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line"],
                data["2016.repayment.3_yr_repayment.overall"]))


def main():
    # main function to hold base URL and call other functions
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
          "id,school.city,school.name,2018.student.size,2017.student.size," \
          "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    # enter url into function to grab data
    all_data = get_data(url)
    # now put data into a database
    conn, cursor = open_db("project_db.sqlite")
    print(type(conn))
    # drop existing table so there are no errors
    #cursor.execute('DROP TABLE IF EXISTS University_Info')
    setup_db(cursor)
    insert_to_database(cursor, all_data)
    close_db(conn)


if __name__ == '__main__':
    main()
