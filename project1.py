# Daniel Kotlinski Sprint 4 adding GUI and data visualization
# 3/14/21


import openpyxl
import requests
import secrets
import sqlite3
import project1GUI
import sys
from PyQt5.QtWidgets import *
import plotly.express as px
from typing import Tuple


def show_figure_collegegrad_vs_job(cursor):
    college_data_list = collegegrad_to_numjobs(cursor)
    locations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                 "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                 "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                 "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                 "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    fig = px.choropleth(locations=locations,
                        locationmode="USA-states", color=college_data_list, scope="usa")

    fig.update_layout(
        title_text='Number of College Graduates vs Number of Jobs Requiring College Degree',
        coloraxis_colorbar=dict(
            title="Num Of Students Per Job")
    )
    fig.show()


def show_figure_declining_balance(cursor):
    # this gets our list of data
    declining_balance_data = declining_balance_to_25percent(cursor)
    locations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                 "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                 "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                 "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                 "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    fig = px.choropleth(locations=locations,
                        locationmode="USA-states", color=declining_balance_data, scope="usa", labels=
                        {'c1_school_closing': 'SCALE'})
    fig.update_layout(
        title_text='Loan Repayment vs Annual 25th Percent Salary',
        coloraxis_colorbar=dict(
            title="Money")
    )

    fig.show()


def display_college_data(data):
    qt_app = QApplication(sys.argv)
    window = project1GUI.Window(data) # sys.argv is the list of command line arguments
    sys.exit(qt_app.exec_())


def declining_balance_to_25percent(cursor):
    # Compare the 3 year graduate cohort declining balance percentage to the 25% salary in the state
    # and visualize that data
    cursor.execute(f'''SELECT AVG(repayment_2016_balance) FROM University_Info group by school_state''')
    repayment_balance = cursor.fetchall()
    repayment_2016 = []
    annual_salary = []
    for data in repayment_balance:
        if data is not None:
            repayment_2016.append(data[0])
    cursor.execute(f'''SELECT AVG(annual_25th_percentile) FROM Employment_Data group by state''')
    annual_percent = cursor.fetchall()
    for newdata in annual_percent:
        annual_salary.append(newdata[0])
    answ = [i / j for i, j in zip(repayment_2016, annual_salary)]
    return answ


def collegegrad_to_numjobs(cursor):
    # get total number of college students per state
    # must prompt user for the abbreviation of what state they wish to look at
    college_grads = []
    num_of_jobs = []
    cursor.execute(f'''SELECT sum(student_size_2018) FROM University_Info group by school_state''')
    num_college_grad = cursor.fetchall()
    for data in num_college_grad:
        college_grads.append(data[0])
    cursor.execute(f'''SELECT sum(jobs_1000)*1000 FROM Employment_Data group by state ''')
    num_jobs_instate = cursor.fetchall()
    for newdata in num_jobs_instate:
        num_of_jobs.append(newdata[0])
    answ = [i / j for i, j in zip(college_grads, num_of_jobs)]
    return answ


def get_data(url: str):
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
    furl = f"{url}&api_key={secrets.api_key}&page=0"
    response = requests.get(furl)
    json_data = response.json()
    meta_data = json_data["metadata"]
    total_data = meta_data.get("total")
    pages = meta_data.get("per_page")
    pagenum = (round(total_data/pages)+1)
    return pagenum


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def create_university_info(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS University_Info(
    id INTEGER PRIMARY KEY,
    school_name TEXT NOT NULL,
    school_state TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT NULL,
    student_size_2017 INTEGER DEFAULT NULL,
    earnings_2017 INTEGER DEFAULT NULL,
    repayment_2016 INTEGER DEFAULT NULL,
    repayment_2016_balance FLOAT DEFAULT NULL
    );''')


def create_employment_data(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employment_Data (
    occ_code TEXT NOT NULL,
    area_type INTEGER NOT NULL,
    state TEXT NOT NULL,
    occupation_major_title TEXT NOT NULL,
    totalemployment_perfield_perstate INTEGER,
    hourly_25th_percentile FLOAT DEFAULT NULL,
    annual_25th_percentile FLOAT DEFAULT NULL,
    o_group TEXT NOT NULL,
    jobs_1000 FLOAT DEFAULT NULL,
    PRIMARY KEY(occ_code, state, occupation_major_title)
    )''')


def web_to_database(cursor: sqlite3.Cursor, all_data):
    for data in all_data:
        if data["school.state"] not in ["PR", "VI", "PW", "MP", "MH", "GU", "FM", "AS", "DC"]:
            cursor.execute('''INSERT INTO University_Info(id, school_state, school_name, school_city, student_size_2018
                    , student_size_2017, earnings_2017, repayment_2016, repayment_2016_balance)
                    VALUES (?,?,?,?,?,?,?,?,?)''', (data["id"], data["school.state"], data["school.name"],
                                                data["school.city"],
                                                data["2018.student.size"],
                                                data["2017.student.size"],
                                                data["2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line"],
                                                data["2016.repayment.3_yr_repayment.overall"],
                                                data["2016.repayment.repayment_cohort.3_year_declining_balance"]))


def excel_to_database(excel_data, cursor: sqlite3.Cursor):
    workbook_file = openpyxl.load_workbook(excel_data)
    worksheet = workbook_file.active
    for data in worksheet.rows:
        o_group = data[9].value
        occupational_code = data[7].value
        area_type = data[2].value
        if o_group == "major":
            if occupational_code[0] != "3" and occupational_code[0] != "4":
                if area_type != "3":
                    state = data[1].value
                    major_title = data[8].value
                    totalemployment_perfield_perstate = data[10].value
                    hourly_25th_percentile = data[19].value
                    annual_25th_percentile = data[24].value
                    jobs_1000 = data[12].value
                    cursor.execute('''INSERT INTO Employment_Data (occ_code, area_type, state, occupation_major_title
                            , totalemployment_perfield_perstate, hourly_25th_percentile, annual_25th_percentile, o_group, 
                                    jobs_1000)
                            VALUES (?,?,?,?,?,?,?,?,?)''', (occupational_code, area_type, state,
                                                        major_title,
                                                        totalemployment_perfield_perstate,
                                                        hourly_25th_percentile,
                                                        annual_25th_percentile, o_group, jobs_1000))


def main():
    #excel_data = "state_M2019_dl.xlsx"
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=" \
          "id,school.state,school.city,school.name,2018.student.size,2017.student.size," \
          "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall,"\
          "2016.repayment.repayment_cohort.3_year_declining_balance"
    #all_data = get_data(url)
    conn, cursor = open_db("project_db.sqlite")
    #cursor.execute('DROP TABLE IF EXISTS University_Info')
    #create_university_info(cursor)
    #cursor.execute('DROP TABLE IF EXISTS Employment_Data')
    #create_employment_data(cursor)
    #excel_to_database(excel_data, cursor)
    #web_to_database(cursor, all_data)
    collegegrad_data = collegegrad_to_numjobs(cursor)
    #declining_balance_to_25percent(cursor)
    display_college_data(collegegrad_data)
    close_db(conn)



if __name__ == '__main__':
    main()
