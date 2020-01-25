from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import *
from selenium.webdriver.common.proxy import *
import json
import gzip
import shutil
from selenium.webdriver.common.keys import Keys
from pprint import pprint

driver =webdriver.Chrome()
driver.set_window_size(1366,768)

ALL_EMOJI=dict()

with open('emoji_score.json') as emoji_unicode:    
    data = json.load(emoji_unicode)

data_array =  data.items()

for i in range(0,751):
	#get unicode
	unicode_char=data_array[i][0]
	unicode_char=unicode_char[2:]
	url_begin="http://www.fileformat.info/info/unicode/char/"
	url_end="/index.htm"
	url=url_begin+str(unicode_char)+url_end
	try:
		driver.get(url)
		js_char=driver.find_element_by_xpath('/html/body/div[3]/div/div/table[4]/tbody/tr[11]/td[2]').text
		js_char=js_char.lower()
		ALL_EMOJI[js_char]=data_array[i][1]
		print "Score mapped for:"+js_char+"\n"

	except Exception:
		print "Webpage was not found\n"
		continue

with open ('emoji_score_js.json','w') as fp:
	json.dump(ALL_EMOJI,fp)

