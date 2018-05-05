from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import csv

#the function below starts the browser and select the correct region
def starts_browser():
    url = 'https://www.lobstersnowboards.com/shop/'

    driver = webdriver.Firefox()

    driver.get(url)

    #select the united states region
    #they get snowboards by your location but there are no sellers available in brazil so I need to chose the region where I want to find snowboards
    driver.find_element_by_xpath("//button[@class='btn dropdown-toggle selectpicker btn-default']").click()
    box_region = driver.find_element_by_xpath("//input[@class='input-block-level form-control']")
    box_region.send_keys("United States");
    box_region.send_keys(Keys.TAB);

    return driver



#the function get all links of snowboard items
def snow_links(driver):
    #get the div that contains snowboards
    div = driver.find_element_by_id("boards_scrollto")

    #get the div that contains special snowboards
    div_spec = driver.find_element_by_class_name('shop-special-additions')

    #get all links of special snowboard products
    links_spec = div_spec.find_elements_by_css_selector('a')
    for i in range(len(links_spec)):
        links_spec[i] =  links_spec[i].get_attribute('href')

    #get all links of snowboard products
    links = div.find_elements_by_css_selector('a')
    for i in range(len(links)):
        links[i] =  links[i].get_attribute('href')

    for i in range(len(links_spec)):
        links.append(links_spec[i])

    return links

def get_information(driver, url_snow, df):

    driver.get(url_snow)
    time.sleep(2)
    url = url_snow

    #get price
    price = driver.find_element_by_class_name("product_price").text
    prices = price.split("\n")
    #sometimes there are two prices, so im taking the last price that is the lowest
    if len(prices)>1:
        price = prices[1]


    #get name
    name = driver.find_element_by_class_name("product-title").text

    #get image
    img = driver.find_element_by_class_name('img-responsive')
    image = img.get_attribute("src");


    #get sizes
    sizes_btn = driver.find_elements_by_xpath("//button[@class='btn dropdown-toggle selectpicker btn-default']")
    sizes_btn[2].click()
    sizes = driver.find_elements_by_xpath("//ul[@class='dropdown-menu inner selectpicker']")

    sizes = sizes[2].text
    sizes.replace("Select","")
    sizes = sizes.split("\n")


    #create the a line with teh same atributtes but with different sizes
    for s in range(len(sizes)):
        if sizes[s].find("Select")==-1:
            df.loc[-1] = [url, name, image, price, sizes[s]]
            df.index = df.index + 1
            df = df.sort_index()

    return df



#create dataframe
df = pd.DataFrame(columns = ['url','name','image','price','size'])

driver = starts_browser()
time.sleep(2)
#get all snowboard product links
url_snows = snow_links(driver)

#access each snowboard product link
for url in url_snows:
    df = get_information(driver, url, df)
    print('Doing ' +str(1+url_snows.index(url))+ ' of ' + str(len(url_snows)))


df.to_csv("results.csv")









