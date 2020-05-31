# Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd


# Set Executable Path
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

# Set Browser
browser = Browser("chrome", **executable_path, headless=True)

# News Function
def news(browser):
    # URL for Scraping
    news_url = "https://mars.nasa.gov/news/"

    # Visit URL
    browser.visit(news_url)

    # Ensure Page Loads
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # Create Beautiful Soup Object
    soup = bs(browser.html, "html.parser")
    
    try:
        # Access the Story
        story = soup.select_one("ul.item_list li.slide")

        # Find News Title
        news_title = story.find("div", class_="content_title").get_text()

        # Find News Paragraph
        news_p = story.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

# Featured Function
def featured(browser):
    # URL for Scraping
    featured_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    
    # Visit URL
    browser.visit(featured_url)

    # Create Beautiful Soup Object
    soup = bs(browser.html, "html.parser")

    try:
        # Access the Picture
        picture = soup.select_one("ul.articles li.slide")

        # Find Mars Picture Partial URL
        mars_pic = picture.find("a", class_="fancybox").get("data-fancybox-href")
    except AttributeError:
        return None
    
    # Set Nasa URL
    nasa_url = "https://www.jpl.nasa.gov"

    # Complete Picture URL
    featured_image_url = f"{nasa_url}{mars_pic}"
    return featured_image_url

# Fact Function
# Mars Facts Web Scraper
def fact():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")
    return mars_table

# Hemisphere Function
def hemisphere(browser):
    # URL for Scraping
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Visit URL
    browser.visit(hemisphere_url)

    # Create List to Hold URLs
    hemisphere_image_urls = []
    
    # Find Links
    links = browser.find_by_css("a.product-item h3")
    # Create For Loop to Get Image URLs
    for link in range(len(links)):
        # Set Empty Dictionary
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[link].click()
        
        # Find Sample Image Anchor Tag
        img = browser.find_link_by_text("Sample").first
    
        # img_url href Key Value Pair
        hemisphere["img_url"] = img["href"]
    
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    
        # Navigate Back
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = bs(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere



def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = news(browser)
    featured_image_url = featured(browser)
    mars_table = fact()
    hemisphere_image_urls = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "fact": mars_table,
        "hemispheres": hemisphere_image_urls
    }
    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape())