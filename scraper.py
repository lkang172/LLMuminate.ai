import requests
from bs4 import BeautifulSoup

def search_pubmed(keywords):
    url = f'https://pubmed.ncbi.nlm.nih.gov/?term={keywords}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    
    page = requests.get(url, headers=headers)
    
    if page.status_code == 403:
        print("Access denied.")
        return []

    soup = BeautifulSoup(page.text, 'html.parser')
    title_divs = soup.find_all('div', class_='docsum-content')
    article_links = []

    for div in title_divs:
        link = div.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            print(href)
            cut_link = href[4:]
            article_links.append(f'https://pubmed.ncbi.nlm.nih.gov{href}')

    return article_links

def search_articles(search_query):
    article_urls = search_pubmed(search_query)
    full_text = []
    
    for url in article_urls:        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        
        page = requests.get(url, headers=headers)
        
        if page.status_code == 403:
            print(f"Access denied for {url}.")
            continue
        
        soup = BeautifulSoup(page.text, 'html.parser')

        section = soup.find('div', class_='abstract-content')

        if section:
            p_tags = section.find_all('p')
            text = [p.get_text(strip=True) for p in p_tags]
            full_text.append(text)
        else:
            print(f'No corresponding section found in {url}')

    return full_text, article_urls

#sample call
'''keywords = [
    "influenza symptom management",
    "hydration flu recovery",
    "over-the-counter flu medications",
    "steam inhalation effectiveness",
    "salt water gargle flu",
    "humidifier respiratory symptoms",
    "nutrition immune system flu",
    "honey antimicrobial properties",
    "antiviral medications influenza",
    "rest immune response",
    "fluid intake respiratory infection"
]'''

# Format the keywords with 'OR' and enclose each in quotes
#formatted_query = ' OR '.join([f'"{keyword}"' for keyword in keywords])
#print(formatted_query)
#print(search_articles(formatted_query))