from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
import json
import gzip
import shutil
from selenium.webdriver.common.keys import Keys

print "Connecting to website....."

service_args = [
    '--proxy=10.3.100.207:8080',
    '--proxy-type=http',
    ]
driver =webdriver.PhantomJS(service_args=service_args)
#driver =webdriver.Chrome()
driver.set_window_size(1366,768)
driver.get('https://appbot.co/login')
driver.implicitly_wait(10)

time.sleep(2)
print "Connected to website"
email=driver.find_element_by_id('user_email')
email.send_keys('pritamtest103@gmail.com')

password=driver.find_element_by_id('user_password')
password.send_keys('test54321')


login_button=driver.find_element_by_xpath('//*[@id="new_user"]/input[5]')
login_button.click()

time.sleep(4)

print "Logged in to website"

driver.implicitly_wait(10)
date_start=25
month_start=5
year_start=2016
ALL_REVIEW=dict()
rev_count=0
emoji_rev=0
emoji_flag=0


danger_flag=0
driver.implicitly_wait(5)
for i in range(1,380):
	

	danger_flag=0


	if date_start == 0:
		date_start= 30
		if month_start == 1:
			month_start = 12
			year_start-=1
		else :
			month_start -=1

	url_start="https://appbot.co/apps/577171-uber/reviews#/?start="+str(year_start)+"-"+str(month_start)+"-"
	url_mid="&end="+str(year_start)+"-"+str(month_start)+"-"
	url_end="&country=134"
	url_full=url_start+str(date_start)+url_mid+str(date_start)+url_end
	wait = WebDriverWait(driver, 15)
	#driver.get('https://appbot.co/apps/568058-instagram/reviews#/?start=2016-03-27&end=2016-03-28&country=134')
	check=0;

	driver.get(url_full)
	
	

	try:
		wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="review-list"]/div/div[3]/div[1]/div[2]')))
	except TimeoutException:
		date_start-=1
		print "Entered TimeoutException 1\n"
		continue
	loop_count =0
	
	while check< 200 :

		loop_count+=1

		if loop_count >= 25:
			break
		for m in range(1,6):
			body = driver.find_element_by_tag_name("body")
  			body.send_keys(Keys.PAGE_DOWN)
		time.sleep(2)
		try:
			review_block=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[3]/div[1]/div[2]')
		except TimeoutException:
			danger_flag=1
			break
			

		all_reviews=review_block.find_elements_by_class_name('review-container')

		count=0;
		for one_review in all_reviews:
			review_content=one_review.find_element_by_class_name('review-date')
		#	print review_content.text
		#	print "\n"
			#review_headline=review_
			count+=1

		#print "..\n"
		#print count
		check=count
		if check == 0:
			danger_flag=1
			print "Entered danger_flag=1 \n"
			break
	#print "now to be Extracted 20 reviews"
	#print check
	if danger_flag ==1:
		date_start-=1
		print "Entered TimeoutException 2\n"
		continue
	review_block=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[3]/div[1]/div[2]')
	all_reviews=review_block.find_elements_by_class_name('review-container')

	count=0;
	for one_review in all_reviews:
			review_basic_att=one_review.find_element_by_class_name('review-basic-attributes')
			review_content=one_review.find_element_by_class_name('review-content')


			#processing attributes

			#extract rating
			#total_rating_tag=review_basic_att.find_elements_by_class_name('icon-star')
			total_rating_tag=review_basic_att.find_elements_by_tag_name("i")
			
			rev_rating=0
			empty_rating=0
			for one_rating_tag in total_rating_tag:
				icon_star_text=one_rating_tag.get_attribute("class")
				#print str(icon_star_text)
				if str(icon_star_text) == "icon-star"  :
					rev_rating+=1
		
			#print "review rating ="+str(rev_rating)+"\n"
			#extract author
			author_tag=review_basic_att.find_element_by_class_name('review-author')
			try:
				author_link=author_tag.find_element_by_tag_name("a")
				rev_author_link=author_link.get_attribute("href")
			except NoSuchElementException:
				rev_author_link =""

			#extract author name	
			rev_author_name=author_tag.text
			#only for author name, rev_subject,rev_body .text is already used

			#extract subject 
			rev_subject=review_content.find_element_by_class_name('review-subject').text


			#extract date
			rev_date=review_content.find_element_by_class_name('review-date')

			#extract review body
			rev_body=review_content.find_element_by_class_name('review-body').text


			body_length=len(rev_body)
			title_length=len(rev_subject)
			emoji_list=list();

			char_list_title = [c for c in rev_subject]
			#extract emojis from title
			emoji_flag=0


			for m in range(0,title_length):
				try:
					char_list_title[m].decode('utf-8')
				except UnicodeEncodeError:
					emoji_list.append(char_list_title[m])
					emoji_flag=1
					char_list_title[m]=u' '
			char_list_title=''.join(char_list_title)
			rev_subject=char_list_title

			#extract emojis from body

			char_list_body = [c for c in rev_body]

			for m in range(0,body_length):
				try:
					char_list_body[m].decode('utf-8')
				except UnicodeEncodeError:
					emoji_list.append(char_list_body[m])
					emoji_flag=1
					char_list_body[m]=u' '

			char_list_body=''.join(char_list_body)
			rev_body=char_list_body


			if emoji_flag == 1:
				emoji_rev+=1

			info=dict()
			
			info['rating']=str(rev_rating)
			info['review_title']=rev_subject
			info['review_date']=rev_date.text.encode('utf-8')
			info['author_name']=rev_author_name.encode('utf8')
			#info['author_link']=rev_author_link
			info['review_body']=rev_body
			info['emoji_list']=emoji_list

			rev_count+=1
			ALL_REVIEW[str(rev_count)]=info
					

			print "Review no:"+ str(rev_count)+"\t extracted \n"

			count+=1
	date_start-=1
	print "Page no :extracted"+ str(i)+"\n"

	
with open ('reviews_uber.json','w') as fp:
	json.dump(ALL_REVIEW,fp)



with open('reviews_uber.json', 'rb') as f_in, gzip.open('reviews_uber.json.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)





