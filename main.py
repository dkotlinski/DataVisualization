# Daniel Kotlinski Sprint1 University Data
# 2/7/21

import requests
import secrets


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

def outputFile(all_data):
    # prints our dictionary to a file
    with open("output.txt", "w") as file_object:
        print(all_data, file=file_object)
        file_object.close()


def main():
    # main function to hold base URL and call other functions
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,school.city,school.name,2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    # enter url into function to grab data
    all_data = get_data(url)
    # now put data into our text file
    outputFile(all_data)

if __name__ == '__main__':
    main()
