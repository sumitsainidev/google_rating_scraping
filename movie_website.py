import xlsxwriter
import imdb
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
chrome_options = Options()
ia = imdb.Cinemagoer()
# top = ia.get_top50_movies_by_genres('sci-fi')
import requests


DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

name = []
googleRating = []
userNoRating = []

tempA = []
for i in range(0,50):
    page_number = i + 1
    url = f"https://bolly4u.tech/page/{page_number}/"


    response = requests.get(url)
    parsed_data = response.text

    soup = BeautifulSoup(parsed_data, 'html.parser')
    div_elements = soup.find_all('div', class_='mt-2 transition-all block px-2 py-3 shadow-inner text-gray-500 group-hover:text-indigo-500 tracking-wide text-sm')
    text_contents = [div.get_text(strip=True) for div in div_elements]

    movies_arr = []

    for text_content in text_contents:
        pattern = r'^[^\d]+ \d{4}'
        matches = re.findall(pattern, text_content, re.MULTILINE)
        if len(matches)>0:
            movies_arr.append(matches[0])

    for i in movies_arr:
    # for i in tempA:
        try:
            # print('checking..',i)
            url = 'https://www.google.com/search?q='+i+' movie reviews'
            driver.get(url)
            
            h1 = driver.find_element(By.XPATH,"//*[contains(text(), 'liked this film')]")
            numOfUserRatings  = 0
            # try:
            #     film_review_element = driver.find_element_by_xpath('//*[@data-ti="FilmReview"]')
            #     film_review_element.click()
            #     print("Element found and clicked.")
            # except e:
            #     pass

            try:
                # Find the div element with the class "H5xxEd" that contains the word "ratings"
                ratings_element = driver.find_element(By.XPATH, '//div[contains(text(), "ratings")]')
    
                # If found, you can perform further actions with this element
                # print("Element found:", ratings_element.text)
                numOfUserRatings = ratings_element.text
            except e:
                b='1'

            likedString = h1.text.replace('%','')
            res = [int(i) for i in likedString.split() if i.isdigit()]
            # print(res)
            name.append(i)
            googleRating.append(res[0])
            userNoRating.append(numOfUserRatings)
            print(i,likedString,numOfUserRatings)
        except Exception as e:
            # print("An exception occurred")
            try:
                h2 = driver.current_url
                if 'sorry/index?' in h2:
                    x = input("Waiting for manual date to be entered. Enter YES when done.")
            except:
                a ='1'
            

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