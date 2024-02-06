import xlsxwriter
import imdb
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
ia = imdb.Cinemagoer()
# top = ia.get_top50_movies_by_genres('sci-fi')
import requests


DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

name = []
googleRating = []

tempA = []
for i in range(50):
    page_number = i + 1
    # url = f"https://api.themoviedb.org/3/movie/now_playing?page={page_number}"
    # url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&page={page_number}&sort_by=popularity.desc&with_original_language=hi&primary_release_date.gte=2022-01-01&primary_release_date.lte=2023-11-01"
    # url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&page={page_number}&sort_by=popularity.desc&primary_release_date.gte=2022-01-01&primary_release_date.lte=2023-12-17"
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&page={page_number}&sort_by=vote_average.desc&release_date.lte=2024-01-12&watch_region=IN&with_original_language=hi&certification_country=IN&release_date.gte=2000-01-01"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmOTEyNTczMTA2MTkyZTc4OWUyZGZlZDFjMGYyOGViMSIsInN1YiI6IjY1NTBmZGM1ZDQ2NTM3MDBmZTM2YWFjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9ZoOHIjlPM94s1GAD92d4rxIk9pJhFbFBXyBN3sO_hY"
    }

    response = requests.get(url, headers=headers)
    parsed_data = json.loads(response.text)
    print(parsed_data)
    for i in parsed_data['results']:
    # for i in tempA:
        try:
            print('checking..',i['title'])
            url = 'https://www.google.com/search?q='+i['title']+' movie'
            driver.get(url)
            
            h1 = driver.find_element_by_xpath("//*[contains(text(), 'liked this film')]")
            likedString = h1.text.replace('%','')
            print(i['title'],likedString)
            res = [int(i) for i in likedString.split() if i.isdigit()]
            # print(res)
            name.append(i['title'])
            googleRating.append(res[0])
        except Exception as e:
            print("An exception occurred")
            try:
                h2 = driver.current_url
                if 'sorry/index?' in h2:
                    x = input("Waiting for manual date to be entered. Enter YES when done.")
            except:
                print("Text not found on the page.")
            continue
            

zipped_lists = zip(googleRating,name)
sorted_pairs = sorted(zipped_lists,reverse=True)

tuples = zip(*sorted_pairs)
googleRating,name = [ list(tuple) for tuple in  tuples]

print(name,googleRating)
workbook = xlsxwriter.Workbook('./bollywood_all_movies_12_01_2024.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Movie Name')
worksheet.write('B1', 'Google Rating')

for index, item in enumerate(name):

    worksheet.write('A'+str(index+2), item)
    worksheet.write('B'+str(index+2), googleRating[index])

workbook.close()