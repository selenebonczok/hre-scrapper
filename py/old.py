# Main webcrawling and webscrapping functions
# dedicated to amnesty sites.

import bs4, requests, os
import pandas as pd
import time


        
def get_website_text(url):
    # A necessary clause: links are improperly 
    # referenced in some of the HTMLs.
    if not url.startswith("https"):
        return None
    try:
        data = connect(url)
        html = bs4.BeautifulSoup(data.text, 'html.parser')
        paragraphs = html.findAll("p")
        text = " \n ".join([x.text for x in paragraphs], )
        return(text)
    except (AttributeError, ConnectionError):
        return(None)

def parse_main_entries(site, tag = "article", props = {"class": "post post--result"}):
    """Finds URLs of each library entry on a year's main website."""

    data = connect(site)
    html = bs4.BeautifulSoup(data.text, 'html.parser')
    elements = html.find_all(tag, props)
    return(elements)

def get_post_characteristics(element):
    """Given a single bs4 result
    configuration of each post in an Amnesty site, extract relevant post
    data."""
    
    link = element.find("a", {"class": "floating-anchor"}).get("href")
    date = element.find("span").text
    title = element.find("h1", {"class": "post-title"}).text
    excerpt = element.find("div", {"class": "post-excerpt"}).text
    props = get_text_and_topics(link)
    topics, text, pdf = props[0], props[1], props[2] #, props[3]
    
    dic = {"Title": title, 
           "Source": "Amnesty Canada (English)",
           "Link": link,
           "Excerpt": excerpt,
           "RawText": text,
           "Tags": topics,
           "Date": date,
           "PDF": pdf
           }
    
    return(pd.DataFrame([dic]))


def get_text_and_topics(url):
    """Given an amnesty publication, get the topics"""

    try:
        data = connect(url)
        html = bs4.BeautifulSoup(data.text, 'html.parser')
        topics_container = html.find("div", {"class": "topics-container"})
        a_topics = topics_container.findAll("a")
        topics = [x.text for x in a_topics]
        paragraphs = html.findAll("p")
        text = " \n".join([x.text for x in paragraphs], )
        pdf = html.find("a", {"class": "btn btn--download btn--dark"})
        return(topics, text, not(pdf is None))#, languages)
    except (AttributeError, ConnectionError):
        return(None, "Inspection flag", False)

def df_from_site(url):
    """Given the URL of an Amensty page, return the dataframe 
    with the properties of each entry in the site."""
    divs = parse_main_entries(url) # ARGUMENTS ARE FOR AUSTRIA
    chars = map(get_post_characteristics, divs)
    dfs = pd.concat(list(chars))
    return(dfs)
    
def connect(url, time_limit = 15):
    success = False
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    timeout = time.time() + time_limit
    while success==False:
        if time.time() > timeout:
            raise ConnectionError
        try:
            content = requests.get(url, headers=headers, timeout=5)
            success=True
        except:
            pass
    return(content) 


def create_data_base(url_head):
    dfs, i = [], 1
    while True:
        try:
            print("At page", str(i), " \n URL: ", url_head + str(i))
            df = df_from_site(url_head + str(i))
            dfs.append(df)
            i += 1
        except:
            return(pd.concat(dfs))
    
    
def create_data_by_pages(url_head, s, n):
    dfs, i = [], s
    for i in range (s, n + 1):
        try:
            print("At page", str(i), " \n URL: ", url_head + str(i))
            df = df_from_site(url_head + str(i))
            dfs.append(df)
            i += 1
        except ValueError:
           break 
    
    return(pd.concat(dfs))