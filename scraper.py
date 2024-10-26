import requests
from bs4 import BeautifulSoup

def search_pubmed(keywords):
    url = f'https://www.ncbi.nlm.nih.gov/pmc/?term={keywords}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    
    page = requests.get(url, headers=headers)
    
    if page.status_code == 403:
        print("Access denied.")
        return []

    soup = BeautifulSoup(page.text, 'html.parser')
    title_divs = soup.find_all('div', class_='title')
    article_links = []

    for div in title_divs:
        link = div.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            cut_link = href[4:]
            article_links.append(f'https://pmc.ncbi.nlm.nih.gov{cut_link}')

    return article_links

def search_articles(search_query):
    article_urls = search_pubmed(search_query)
    full_text = []
    
    for url in article_urls[:5]:        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        
        page = requests.get(url, headers=headers)
        
        if page.status_code == 403:
            print(f"Access denied for {url}.")
            continue
        
        soup = BeautifulSoup(page.text, 'html.parser')

        section = soup.find('section', class_='body main-article-body')

        if section:
            p_tags = section.find_all('p')
            text = [p.get_text(strip=True) for p in p_tags]
            full_text.append(text)
        else:
            print(f'No corresponding section found in {url}')

    return full_text

#sample call
print(search_articles("cancer treatment chemo"))
