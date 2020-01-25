# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import *
# from selenium.webdriver.common.proxy import *
import json
import gzip
import shutil
# from selenium.webdriver.common.keys import Keys
from pprint import pprint

from nltk.sentiment.vader import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()
ALl_REVIEWS=dict()

with open('reviews_lyft_10days.json') as emoji_unicode:    
    data = json.load(emoji_unicode)

print("file 1 read")

with open('emoji_score_js.json') as emoji_unicode:    
    data_emoji_score = json.load(emoji_unicode)
print("file 2 read")

data_emoji_score_array=data_emoji_score.items()
total_emoji=len(data_emoji_score_array)


match_count = 0
for i in range(1, len(data.keys())+1):
	info = data[str(i)]
	#extract sentiment score from text data
	score_body = analyzer.polarity_scores(info['review_body'])
	score_title = analyzer.polarity_scores(info['review_title'])
	rev_text_score =  float(score_body['compound']) + float(score_title['compound'])

	#extract emoji sentiment score

	emoji_list = info['emoji_list']
	rev_emoji_score=0.00
	j = 0

	while j < len(emoji_list)-1:

		emoji_one=emoji_list[j]
		emoji_two=emoji_list[j+1]

		success_flag=0

		for k in data_emoji_score.keys():
			#print("")
			emoji_list_length=len(k)

			if emoji_list_length == 9:
				#emoji_score_one = data_emoji_score_array[k][0]
				emoji_score_one = k

				if emoji_one in k:
					print("match found for single length emoji")
					match_count += 1
					rev_emoji_score=rev_emoji_score+float(data_emoji_score[k])
					success_flag=1
					j+=1
					break


			if emoji_list_length == 14:
				#emoji_score_one=data_emoji_score_array[k][0][3:7]
				#emoji_score_two=data_emoji_score_array[k][0][9:13]
				
				
				emoji_score_one = k[3:7]
				emoji_score_two = k[9:13]
				if emoji_one in k:
					if  emoji_two in k:		
						print("match found for double length emoji")	
						match_count += 1	
						rev_emoji_score=rev_emoji_score+float(data_emoji_score[k])
						success_flag=1
						j+=2
						break


		if success_flag == 0:
			j+=1
		

	print ("review no -%s- processed | " % str(i))
	#print("Emoji score = %s" % str(rev_emoji_score))
	info['emoji_score'] = str(rev_emoji_score)
	info['text_score'] = str(rev_text_score)

	ALl_REVIEWS[str(i)] = info



with open ('reviews_lyft_with_score_mid.json','w') as fp:
	json.dump(ALl_REVIEWS,fp)


with open('reviews_lyft_with_score_mid.json', 'rb') as f_in, gzip.open('reviews_lyft_with_score_mid.json.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)

print ("no of matched %s" % str(match_count))