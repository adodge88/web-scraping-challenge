from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    main_dict = {}

## NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    main_dict["title"] = soup.find("article").find("div",class_='content_title').a.text
    main_dict["news_p"] = soup.find("article").find("div",class_='article_teaser_body').text

    #close  browser
    browser.quit()

## JPL Mars Space Images - Featured Image
    main_url = 'https://www.jpl.nasa.gov'
    query_url = main_url + '/spaceimages/?search=&category=Mars'
    browser.visit(query_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #find the image
    article_style = soup.find("article")['style']
    #extract the url from the background img style
    featured_image_link = article_style.split("'")[1].split("'")[0]

    main_dict["featured_image_url"] = main_url + featured_image_link

    #close  browser
    browser.quit()

## Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('div', class_="js-tweet-text-container")
    result = results[0]

    main_dict["mars_weather"] = result.find('p').text

## Mars Facts
    url = 'https://space-facts.com/mars/'

    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[0]
    mars_facts_df = mars_facts_df.rename(columns={0:'fact type',1:'fact'})

    main_dict["mars_facts"] = mars_facts_df.to_dict('records')
    
    ## Mars Hemisphere
    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a', class_="itemLink")

    hemi_img_url = {}
    hemisphere_image_urls = []

    for result in results:
        try:
            title = result.find('h3').text
            image_link = base_url + result['href']
            
            if (title and image_link):
                hemi_img_url = {
                    'title': title,
                    'image_url': image_link
                }
                hemisphere_image_urls.append(hemi_img_url)

        except AttributeError:
            print('x')
    
    main_dict["mars_hemispheres"] = hemisphere_image_urls

    return main_dict
