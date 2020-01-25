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
    '--proxy-type=https',
    ]
# driver =webdriver.PhantomJS(service_args=service_args)
# driver =webdriver.PhantomJS()
driver =webdriver.Chrome('C:\Chromedriver\chromedriver.exe')
# driver =webdriver.Firefox()

driver.set_window_size(1366,768)

driver.get('https://appbot.co/login')
# driver.get('https://www.google.com')
driver.implicitly_wait(10)

time.sleep(2)
print "Connected to website"
email=driver.find_element_by_id('user_email')
email.send_keys('pritamtest107@gmail.com')

password=driver.find_element_by_id('user_password')
password.send_keys('test54321')


login_button=driver.find_element_by_xpath('//*[@id="new_user"]/div[3]/input')
login_button.click()

time.sleep(4)

print "Logged in to website"

driver.implicitly_wait(10)
date_start=29
month_start=2
year_start=2016
ALL_REVIEW=dict()
rev_count=0
emoji_rev=0
emoji_flag=0


danger_flag=0
driver.implicitly_wait(5)
for i in range(1,241):
	

	danger_flag=0


	if date_start == 0:
		date_start= 30
		if month_start == 1:
			month_start = 12
			year_start-=1
		else :
			month_start -=1

	url_start="https://appbot.co/apps/638224-amazon-shopping/reviews#/?start="+str(year_start)+"-"+str(month_start)+"-"
	url_mid="&end="+str(year_start)+"-"+str(month_start)+"-"
	url_end="&country=134"
	url_full=url_start+str(date_start)+url_mid+str(date_start)+url_end
	wait = WebDriverWait(driver, 15)
	#driver.get('https://appbot.co/apps/568058-instagram/reviews#/?start=2016-03-27&end=2016-03-28&country=134')
	check=0;

	driver.get(url_full)
	
	time.sleep(10)
#################################################################################################################
	try:
		wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="review-list"]/div/div[2]/div[1]/span[2]')))
	except TimeoutException:
		date_start-=1
		print "Entered TimeoutException 1\n"
		continue
####################################################################################################################

#####################################################################################################################
	total_rev=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[2]/div[1]/span[2]').text# total reviews

	five_rev=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[2]/div[3]/table/tbody/tr[1]/td[3]').text#5 star reviews
	four_rev=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[2]/div[3]/table/tbody/tr[2]/td[3]').text#4 star reviews
	three_rev=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[2]/div[3]/table/tbody/tr[3]/td[3]').text#3 star reviews
	two_rev=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[2]/div[3]/table/tbody/tr[4]/td[3]').text#2 star reviews
	one_rev=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[2]/div[3]/table/tbody/tr[5]/td[3]').text#1 star reviews

	print "Total ratings="+str(total_rev)
	print "1-star="+str(one_rev)+" || 2-star="+str(two_rev)+" || 3-star="+str(three_rev)+" || 4-star="+str(four_rev)+" || 5-star="+str(five_rev)
	info=dict()
	info['1_star']=one_rev
	info['3_star']=two_rev
	info['3_star']=three_rev
	info['4_star']=four_rev
	info['5_star']=five_rev
	info['total']=total_rev
	info['date']=str(date_start)+"_"+str(month_start)+"_"+str(year_start)

	rev_count+=1
	date_start-=1
	ALL_REVIEW[str(rev_count)]=info

	if rev_count % 100 == 0:
				with open ('rating_ebay_backup.json','w') as fp:
					json.dump(ALL_REVIEW,fp)


with open ('rating_ebay.json','w') as fp:
	json.dump(ALL_REVIEW,fp)



with open('rating_ebay.json', 'rb') as f_in, gzip.open('rating_ebay.json.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)

#####################################################################################################################
# 	loop_count =0
	
# 	while check< 200 :

# 		loop_count+=1

# 		if loop_count >= 25:
# 			break
# 		for m in range(1,6):
# 			body = driver.find_element_by_tag_name("body")
#   			body.send_keys(Keys.PAGE_DOWN)
# 		time.sleep(2)
# 		print "Scrolling down.."
# 		print str(check)
# 		try:
# 			review_block=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[3]/div[1]/div[2]')
# 		except TimeoutException:
# 			danger_flag=1
# 			break
			
# 		try:
# 			all_reviews=review_block.find_elements_by_class_name('review-container')
# 		except Exception as e:
# 			continue

# 		count=0;
# 		for one_review in all_reviews:
# 			try:
# 				review_content=one_review.find_element_by_class_name('review-date')
# 			except Exception as e:
# 				break
# 		#	print review_content.text
# 		#	print "\n"
# 			#review_headline=review_
# 			count+=1

# 		#print "..\n"
# 		#print count
# 		check=count
# 		if check == 0:
# 			danger_flag=1
# 			print "Entered danger_flag=1 \n"
# 			break
# 	#print "now to be Extracted 20 reviews"
# 	#print check
# 	if danger_flag ==1:
# 		date_start-=1
# 		print "Entered TimeoutException 2\n"
# 		continue
# 	try:
# 		review_block=driver.find_element_by_xpath('//*[@id="review-list"]/div/div[3]/div[1]/div[2]')
# 	except Exception as e:
# 		continue

# 	all_reviews=review_block.find_elements_by_class_name('review-container')

# 	count=0;
# 	for one_review in all_reviews:
# 			review_basic_att=one_review.find_element_by_class_name('review-basic-attributes')
# 			review_content=one_review.find_element_by_class_name('review-content')


# 			#processing attributes

# 			#extract rating
# 			#total_rating_tag=review_basic_att.find_elements_by_class_name('icon-star')
# 			total_rating_tag=review_basic_att.find_elements_by_tag_name("i")
			
# 			rev_rating=0
# 			empty_rating=0
# 			for one_rating_tag in total_rating_tag:
# 				icon_star_text=one_rating_tag.get_attribute("class")
# 				#print str(icon_star_text)
# 				if str(icon_star_text) == "icon-star"  :
# 					rev_rating+=1
		
# 			#print "review rating ="+str(rev_rating)+"\n"
# 			#extract author
# 			author_tag=review_basic_att.find_element_by_class_name('review-author')
# 			try:
# 				author_link=author_tag.find_element_by_tag_name("a")
# 				rev_author_link=author_link.get_attribute("href")
# 			except NoSuchElementException:
# 				rev_author_link =""

# 			#extract author name	
# 			rev_author_name=author_tag.text
# 			#only for author name, rev_subject,rev_body .text is already used

# 			#extract subject 
# 			rev_subject=review_content.find_element_by_class_name('review-subject').text


# 			#extract date
# 			try:
# 				rev_date=review_content.find_element_by_class_name('review-date')
# 			except Exception:
# 				rev_date = ""
# 			#extract review body
# 			rev_body=review_content.find_element_by_class_name('review-body').text


# 			body_length=len(rev_body)
# 			title_length=len(rev_subject)
# 			emoji_list=list();

# 			char_list_title = [c for c in rev_subject]
# 			#extract emojis from title
# 			emoji_flag=0


# 			for m in range(0,title_length):
# 				try:
# 					char_list_title[m].decode('utf-8')
# 				except UnicodeEncodeError:
# 					emoji_list.append(char_list_title[m])
# 					emoji_flag=1
# 					char_list_title[m]=u' '
# 			char_list_title=''.join(char_list_title)
# 			rev_subject=char_list_title

# 			#extract emojis from body

# 			char_list_body = [c for c in rev_body]

# 			for m in range(0,body_length):
# 				try:
# 					char_list_body[m].decode('utf-8')
# 				except UnicodeEncodeError:
# 					emoji_list.append(char_list_body[m])
# 					emoji_flag=1
# 					char_list_body[m]=u' '

# 			char_list_body=''.join(char_list_body)
# 			rev_body=char_list_body


# 			if emoji_flag == 1:
# 				emoji_rev+=1

# 			info=dict()
			
# 			info['rating']=str(rev_rating)
# 			info['review_title']=rev_subject
# 			info['review_date']=rev_date.text.encode('utf-8')
# 			info['author_name']=rev_author_name.encode('utf8')
# 			#info['author_link']=rev_author_link
# 			info['review_body']=rev_body
# 			info['emoji_list']=emoji_list

# 			rev_count+=1
# 			ALL_REVIEW[str(rev_count)]=info
					
# 			if rev_count % 1000 == 0:
# 				with open ('reviews_ebay_backup.json','w') as fp:
# 					json.dump(ALL_REVIEW,fp)
# 			print "Review no:"+ str(rev_count)+"\t extracted \n"

# 			count+=1
# 	date_start-=1
# 	print "Page no :extracted"+ str(i)+"\n"

	
# with open ('reviews_ebay.json','w') as fp:
# 	json.dump(ALL_REVIEW,fp)



# with open('reviews_ebay.json', 'rb') as f_in, gzip.open('reviews_ebay.json.gz', 'wb') as f_out:
#     shutil.copyfileobj(f_in, f_out)





