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



with open('rev_only_emoji.json') as emoji_unicode:    
    data_emoji = json.load(emoji_unicode)

#print data_emoji["16701"][0]



with open('emoji_score_js.json') as emoji_unicode:    
    data_emoji_score = json.load(emoji_unicode)
data_emoji_score_array=data_emoji_score.items()
print data_emoji_score_array[11][0][3:7]
#print len("\"\\ud83c\\udf56\"")

hold="\"\\ud83c\\udf56\""
#print hold[3:7]
#print hold[9:13]


hold2="u\"\\u2604\""
#print hold2[4:8]



#end of tests

success_flag=0
rev_emoji_score=0.00
total_emoji=len(data_emoji_score_array)
REV_EMOJI_SCORE=dict()

rev_with_emoji_count=0

for i in range(1,22961):
	emoji_list=data_emoji[str(i)]
	rev_emoji_score=0.00
	j=0
	while j < len(emoji_list)-1:

		emoji_one=emoji_list[j]
		emoji_two=emoji_list[j+1]
		print "emoji_one is :"+emoji_one+"\n"
		print "emoji_two is :"+emoji_two+"\n"
		
		success_flag=0

		for k in range(0,total_emoji):

			emoji_list_length=len(data_emoji_score_array[k][0])

			if emoji_list_length == 9:
				emoji_score_one = data_emoji_score_array[k][0]
				print "emoji_test_one in small length is :"+emoji_score_one[4:8]+"\n"
		
				if emoji_one == emoji_score_one[4:8]:
					rev_emoji_score=rev_emoji_score+float(data_emoji_score_array[k][1])
					success_flag=1
					print "1st success_flag =1 for i="+str(i)+"\n"
					j+=1
					break

				

			if emoji_list_length == 14:
				emoji_score_one=data_emoji_score_array[k][0][3:7]
				emoji_score_two=data_emoji_score_array[k][0][9:13]
				print "emoji_test_one in big length is :"+emoji_one+"\n"
				print "emoji_test_two in big length is :"+emoji_two+"\n"
		
				

				if emoji_one == emoji_score_one:
					if  emoji_two == emoji_score_two:				
						rev_emoji_score=rev_emoji_score+float(data_emoji_score_array[k][1])
						success_flag=1
						print "2nd success_flag =1 for i="+str(i)+"\n"
						j+=2
						break

		if success_flag == 0:
			j+=1
		


	print "review no"+str(i)+"processed\n"
	REV_EMOJI_SCORE[str(i)] = str(rev_emoji_score)





with open ('rev_emoji_score_final.json','w') as fp:
	json.dump(REV_EMOJI_SCORE,fp)







'''
ALL_EMOJI=dict()

ALL_EMOJI["one"]="test_one"
ALL_EMOJI["two"]="test_two"
ALL_EMOJI["three"]="test_three"



with open ('test.json','w') as fp:
	json.dump(ALL_EMOJI,fp)

#time.sleep()


with open('emoji_score_js.json') as emoji_unicode:    
    data_emoji = json.load(emoji_unicode)
data_array_emoji=data_emoji.items()
print data_array_emoji[0][0][3:7]
print data_array_emoji[0][0][9:13]


with open('reviews.json') as emoji_unicode:    
    data_rev = json.load(emoji_unicode)

data_array_rev=data_rev.items()

#16701

emoji_list = data_rev["16701"]["emoji_list"]

hold= emoji_list[0]



print hold



print "done"

REV_ONLY_EMOJI=dict()

for i in range(1,22961):

	emoji_list = data_rev[str(i)]["emoji_list"]
	REV_ONLY_EMOJI[str(i)]=emoji_list

	


with open ('rev_only_emoji.json','w') as fp:
	json.dump(REV_ONLY_EMOJI,fp)


	'''




		