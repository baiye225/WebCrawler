
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time, os
import urllib
import urllib.request
import socket
import json




# Initialize seaching keyword and search engine(url)
search_input = 'dota2'
url = 'https://www.google.com/'

# Initialize xpath(reverse analysis)
xpath 				= '//div[@style="visibility: inherit;"]/div/a/img' 
click_path 			= '//input[@value="Show more results"]'
google_seaerch_path = '//input[@title="Search"]'
results_image_path  = '//div[@id="top_nav"]//div[@id="hdtb-msb-vis"]//a[@class="q qs"]' 

# Launching Internet Explorer
print('Launch Internet Explorer...')
driver = webdriver.Firefox()
 
# Maximize the Window
print('Maximize the Window...')
driver.maximize_window()
 
# Load "Image Url List.json". 
# If "Image Url List" is not exist, then initialize it.
print('Initialize Image Pool...')

try:
	f = open("ImageUrlList.json", "r")
	img_url_dic = json.load(f)
	f.close()
	os.remove('./ImageUrlList.json')
except:
	img_url_dic = {}


# Load HTML Page
print('Load HTML Page...')
driver.get(url)

# Type keywords and "Enter" in main page of the search engine
search_box = driver.find_elements_by_xpath(google_seaerch_path)[0]
search_box.send_keys(search_input)
search_box.send_keys(Keys.RETURN)

time.sleep(5) # give enough time for webdriver to load html page

# Redirect into "Images" page
## Find position of the "Images"
results_image_pos = driver.find_elements_by_xpath(results_image_path)[2] 
## Click the "Images"
ActionChains(driver).move_to_element(results_image_pos).click(results_image_pos).perform() 
 
# Initialize parameters
pos 	  = 0  # position of scroll down
n 		  = 14 # the times of scroll down 
m 		  = 0  # the current number of downloaded files
m_faired  = 0  # the current number of faired downloaded files
m_timeout = 0  # the current number of timeout downloaded files

# Scoll down page and try to get more source code(async loading)
for i in range(n):
	# scroll down
	print("Try to scroll page(%d/%d)" %((i+1),n))
	pos += i*500 # scroll down 500 per times
	js = "document.documentElement.scrollTop=%d" % pos
	try :
		driver.execute_script(js)
		time.sleep(1)
	except:
		break

	# try to click "show more results"
	try:
		click_pos = driver.find_elements_by_xpath(click_path)[0]
		ActionChains(driver).move_to_element(click_pos).click(click_pos).perform()
		print("Click [show more results]")
		time.sleep(1)
	except:
		continue

# Find js elements related to images by using xpath
elements = driver.find_elements_by_xpath(xpath)
elements_lenth = len(elements)

# setup time limitation
socket.setdefaulttimeout(30)

# Download images from url of each image element
for element in elements:
	img_url = element.get_attribute('src')

	# check the url of the image and download it
	if img_url != None and img_url not in img_url_dic:
		img_url_dic[img_url] = ''

		# download image
		folder_dir = "/home/ye/YePython/crawler1/download/"
		img_name = img_url[img_url.rfind('/') + 1:len(img_url)] + '.jpg'
		download_dir = folder_dir + img_name
		
		print('Try to download: %s' %img_name)


		try:	
			urllib.request.urlretrieve(img_url, download_dir)
			print("%d/%d is downloaded" %(m,elements_lenth))
			m += 1
		except  socket.timeout:
			print("timeout!!!")
			m_timeout += 1
			continue
		except:
			print("failed to download %s !!!" % img_name)
			m_faired += 1
			continue

# summarize downloading result
print("download is completed!!!")
print("%d images are downloaded\n%d images are faied to download\n \
%d images are timeout to download" %(m, m_faired, m_timeout))

# rewrite "ImageUrlList.json"
f = open("ImageUrlList.json", "w")
f.write(json.dumps(img_url_dic))
f.close() 

