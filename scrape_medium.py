import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_medium_articles(username, max_articles=10):
    base_url = f"https://medium.com/@{username}/latest"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    articles = []
    res = requests.get(base_url, headers=headers)
    
    if res.status_code != 200:
        print(f"Failed to access page: {base_url}")
        return

    soup = BeautifulSoup(res.content, 'html.parser')

    # Find all article links, explicitly exclude unwanted URLs
    article_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if (f"/@{username}/" in href # Get rid of irrelevent links
            and "?source=" in href
            and not any(x in href for x in ["/about", "/followers", "/following"])): # Get rid of /about, /followers, and \following page
            
            full_link = href.split('?')[0]
            if full_link.startswith("https://medium.com") or full_link.startswith(f"/@{username}/"):
                # Ensure absolute URL
                if not full_link.startswith("https://medium.com"):
                    full_link = "https://medium.com" + full_link
                article_links.append(full_link)

    # Remove duplicates
    article_links = list(set(article_links))

    if not article_links:
        print(f"No articles found for @{username}. Check the profile manually.")
        return

    # Scrape each article
    scraped_count = 0
    for url in article_links:
        if scraped_count >= max_articles:
            break
        print(f"Scraping article: {url}")
        article_res = requests.get(url, headers=headers)

        if article_res.status_code != 200:
            print(f"Failed to access article: {url}")
            continue

        article_soup = BeautifulSoup(article_res.content, 'html.parser')

        title = article_soup.find('h1')
        title_text = title.get_text(strip=True) if title else 'No title'

        paragraphs = article_soup.find_all('p')
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        articles.append({
            "title": title_text,
            "url": url,
            "content": content
        })

        scraped_count += 1
        time.sleep(1)  # Be polite to Medium's servers

    # Save to CSV
    df = pd.DataFrame(articles)
    df.to_csv(f"{username}_medium_articles.csv", index=False)

    print(f"Scraped {len(df)} articles from Medium user @{username}")

# Example usage:
get_medium_articles("ayanaeliza", max_articles=10)
get_medium_articles("iris4action", max_articles=50)