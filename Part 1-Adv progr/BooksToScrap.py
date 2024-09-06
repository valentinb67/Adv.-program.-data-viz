import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#Création d'une fonction permettant de scraper toutes les pages contenant les informations à scrapper sur les festivals 
def get_all_pages():
    urls = []
    page_number = 0
    for i in range(1, 50):
        url = f"https://books.toscrape.com/catalogue/page-2{page_number}.html"
        page_number += 1
        urls.append(url)
    return urls

url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
r = requests.get(url)
soup = BeautifulSoup(r.content, features="lxml")
books = soup.find_all(ol class="row")
print(books)

def get_books_names(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    books = soup.find_all("tr")
    data = []
    for book in Books[1:]:
        Books = {}
        Books['Name_Book'] = book.find("td",
                                                   headers="view-title-table-column",
                                                   class_="views-field views-field-title is-active").text.strip() if festival.find("td", 
                                                                                                                                   headers="view-title-table-column",
                                                                                                                                   class_="views-field views-field-title is-active") else ""
        Books['Grade'] = book.find("td",
                                                      headers="view-field-city-table-column",
                                                      class_="views-field views-field-field-city").text.strip() if festival.find("td",
                                                                                                                                 headers="view-field-city-table-column",
                                                                                                                                 class_="views-field views-field-field-city") else ""
        Books['Price'] = book.find("td",
                                                      headers="view-field-state-region-table-column",
                                                      class_="views-field views-field-field-state-region").text.strip() if festival.find("td",
                                                                                                                                         headers="view-field-state-region-table-column",
                                                                                                                                         class_="views-field views-field-field-state-region") else ""
        Books['Pays_Event'] = book.find("td",
                                                    headers="view-field-country-table-column",
                                                    class_="views-field views-field-field-country").text.strip() if festival.find("td",
                                                                                                                                  headers="view-field-country-table-column",
                                                                                                                                  class_="views-field views-field-field-country") else ""
        data.append(Books)
    return data