# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    #soup/set up and define browser
    browser = init_browser()
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #scrape titles and paragraphs
    heading = soup.find_all('div', class_='content_title')
    news_title = heading[0].text
    p_text = soup.find_all('div', class_='article_teaser_body')
    news_p = p_text[0].text

    
    #setup
    browser.visit('https://spaceimages-mars.com/')
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    #scrape for results and images
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #image source path
    results = soup.find_all('figure', class_='lede')
    img_path = results[0].a['href']
    featured_image = 'https://www.jpl.nasa.gov' + img_path

    #create tables
    tables = pd.read_html('https://galaxyfacts-mars.com/')
    df = tables[1]
    df.columns=['description', 'value']
    
    #table converted to html
    mars_facts_table = df.to_html(classes='data table', index=False, header=False, border=0)

    #visit next site
    browser.visit('https://marshemispheres.com/')    
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = []

    #search for results in each table
    results = soup.find_all('div', class_="collapsible results")
    hemi_names = results[0].find_all('h3')

    #itereate through hemi's
    for name in hemi_names:
        hemispheres.append(name.text)

    #thumbnail link search
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:
        
        if (thumbnail.img):
            
            thumbnail_url = 'https://marshemispheres.com/' + thumbnail['href']
            
            thumbnail_links.append(thumbnail_url)
    
    imgs = []

    for url in thumbnail_links:       
        browser.visit(url)   
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #scrape from each page
        results = soup.find_all('img', class_='wide-image')
        img_path = results[0]['src']
        
        img_link = 'https://marshemispheres.com/' + img_path
        
        #append orgiinal list
        imgs.append(img_link)

    #zip together
    mars_zip = zip(hemisphres, imgs)

    hemisphere_image_urls = []

    #loops thourhhg
    for title, img in mars_zip:
        
        mars__dict = {}        
        mars__dict['title'] = title
        mars__dict['img_url'] = img
        
        hemisphere_image_urls.append(mars_dict)
    

    # create master dictonary for all data
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image,
        "mars_facts": mars_facts_table,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data