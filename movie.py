import xlsxwriter
import imdb
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
ia = imdb.Cinemagoer()
# top = ia.get_top50_movies_by_genres('sci-fi')
top = ia.get_top250_indian_movies()
# print(top)

DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

name = []
googleRating = []

tempA = []
tempA.append(top[0])
tempA.append(top[1])
tempA.append(top[2])
tempA.append(top[4])
tempA.append(top[5])
for i in top:
# for i in tempA:
    try:
        print('checking..',i.data['title'])
        url = 'https://www.google.com/search?q='+i.data['title']
        driver.get(url)
        h1 = driver.find_element_by_xpath("//div[contains(@class, 'a19vA')]/span")
        likedString = h1.text.replace('%','')
        print(i.data['title'],likedString)
        res = [int(i) for i in likedString.split() if i.isdigit()]
        # print(res)
        name.append(i.data['title'])
        googleRating.append(res[0])
    except Exception as e:
        print("An exception occurred",e)
        x = input("Waiting for manual date to be entered. Enter YES when done.")
        continue
            

zipped_lists = zip(googleRating,name)
sorted_pairs = sorted(zipped_lists,reverse=True)

tuples = zip(*sorted_pairs)
googleRating,name = [ list(tuple) for tuple in  tuples]

print(name,googleRating)
workbook = xlsxwriter.Workbook('./best_indian_movies.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Movie Name')
worksheet.write('B1', 'Google Rating')

for index, item in enumerate(name):

    worksheet.write('A'+str(index+2), item)
    worksheet.write('B'+str(index+2), googleRating[index])

workbook.close()