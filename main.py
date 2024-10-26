from bs4 import BeautifulSoup
import requests

def search_pubmed(keywords):
    url = f'https://www.ncbi.nlm.nih.gov/pmc/?term={keywords}';
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    #print(soup.prettify())

    title_divs = soup.find_all('div', class_='title')
    article_links = []

    for div in title_divs:
        link = div.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            cut_link = href[4:len(href)]
            article_links.append(f'https://pmc.ncbi.nlm.nih.gov{cut_link}')

    return article_links

article_urls = search_pubmed("cancer")

for url in article_urls:
    print(url)