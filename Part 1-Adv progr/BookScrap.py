import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL du site
BASE_URL = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
BOOKS_BASE_URL = 'https://books.toscrape.com/catalogue/'

# Fonction pour récupérer les URLs des livres sur la page principale
def get_book_links(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Error fetching page {page_url}, status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    book_links = []
    
    # Sélectionner les liens vers les pages des livres
    for article in soup.find_all('article', class_='product_pod'):
        link = article.find('h3').find('a')['href']
        # Utiliser urljoin pour construire l'URL absolue du livre
        absolute_link = urljoin(BOOKS_BASE_URL, link)
        book_links.append(absolute_link)
    
    return book_links

# Fonction pour scraper les détails d'un livre avec vérifications
def scrape_book_details(book_url):
    response = requests.get(book_url)
    if response.status_code != 200:
        print(f"Error fetching book page {book_url}, status code: {response.status_code}")
        return {
            'title': '404 Not Found',
            'price': 'No Price',
            'availability': 'No Availability',
            'upc': 'No UPC',
            'product_type': 'No Type',
            'tax': 'No Tax'
        }
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraire les informations spécifiques d'un livre avec des vérifications
    title = soup.find('h1').text if soup.find('h1') else 'No Title'
    price = soup.find('p', class_='price_color').text if soup.find('p', class_='price_color') else 'No Price'
    availability = soup.find('p', class_='instock availability').text.strip() if soup.find('p', class_='instock availability') else 'No Availability'
    
    # Extraire les informations supplémentaires comme la description et la catégorie
    product_info = soup.find_all('td')
    
    if len(product_info) >= 5:
        upc = product_info[0].text
        product_type = product_info[1].text
        tax = product_info[4].text
    else:
        upc = 'No UPC'
        product_type = 'No Type'
        tax = 'No Tax'
    
    book_details = {
        'title': title,
        'price': price,
        'availability': availability,
        'upc': upc,
        'product_type': product_type,
        'tax': tax
    }
    
    return book_details

# Fonction pour scrapper tous les livres d'une page
def scrape_books_from_page(page_url):
    books = []
    book_links = get_book_links(page_url)
    
    # Parcourir chaque lien pour scraper les détails des livres
    for book_url in book_links:
        book_details = scrape_book_details(book_url)
        books.append(book_details)
    
    return books

# Fonction pour gérer la pagination et scraper toutes les pages
def scrape_all_books(base_url):
    page_url = base_url
    all_books = []
    
    while page_url:
        books = scrape_books_from_page(page_url)
        all_books.extend(books)
        
        # Pagination - Trouver le lien "Next"
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Error fetching page {page_url}, status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        next_button = soup.find('li', class_='next')
        
        if next_button:
            next_page_url = next_button.find('a')['href']
            page_url = urljoin(BASE_URL, next_page_url)
        else:
            page_url = None  # Fin de la pagination
    
    return all_books

# Scraper tous les livres à partir de la première page
books_data = scrape_all_books(BASE_URL)

# Affichage des résultats
for book in books_data:
    print(book)



