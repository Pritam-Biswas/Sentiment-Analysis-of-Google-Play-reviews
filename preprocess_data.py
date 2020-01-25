import json
import gzip
import shutil
import xmltodict
from sets import Set
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re


FEATURE=dict()
NORM_FEATURE=dict()
DAY=dict()

## globals ###

def getMin(one,two,three,four,five):
	min1=min(one,two)
	min2=min(three,four)
	min12=min(min1,min2)
	min_val=min(min12,five)
	return min_val

def editDataSet():
	global FEATURE
	one_count=0
	two_count=0
	three_count=0
	four_count=0
	five_count=0

	for i in FEATURE.keys():
		if FEATURE[i]['rating'] == '1':
			one_count+=1
		if FEATURE[i]['rating'] == '2':
			two_count+=1
		if FEATURE[i]['rating'] == '3':
			three_count+=1
		if FEATURE[i]['rating'] == '4':
			four_count+=1
		if FEATURE[i]['rating'] == '5':
			five_count+=1

	min_count=getMin(one_count,two_count,three_count,four_count,five_count)
	print "Before exit loop :"
	print "one_count :"+str(one_count)
	print "two_count :"+str(two_count)
	print "three_count :"+str(three_count)
	print "four_count :"+str(four_count)
	print "five_count :"+str(five_count)
	print " ##############################"
	print "min_count :"+str(min_count)
	

	one_count=0
	two_count=0
	three_count=0
	four_count=0
	five_count=0

	count=1
	for i in FEATURE.keys():

		if count > 5*min_count:
			break

		if FEATURE[i]['rating'] == '1':
			if one_count < min_count:
				NORM_FEATURE[str(count)]=FEATURE[i]
				count+=1
				one_count+=1

		if FEATURE[i]['rating'] == '2':
			if two_count < min_count:
				NORM_FEATURE[str(count)]=FEATURE[i]
				count+=1
				two_count+=1

		if FEATURE[i]['rating'] == '3':
			if three_count < min_count:
				NORM_FEATURE[str(count)]=FEATURE[i]
				count+=1
				three_count+=1

		if FEATURE[i]['rating'] == '4':
			if four_count < min_count:
				NORM_FEATURE[str(count)]=FEATURE[i]
				count+=1
				four_count+=1

		if FEATURE[i]['rating'] == '5':
			if five_count < min_count:
				NORM_FEATURE[str(count)]=FEATURE[i]
				count+=1
				five_count+=1

	print "After exit loop :"
	print "one_count :"+str(one_count)
	print "two_count :"+str(two_count)
	print "three_count :"+str(three_count)
	print "four_count :"+str(four_count)
	print "five_count :"+str(five_count)
	print " ##############################"
	print "min_count :"+str(min_count)

		

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return filtered_words

with open('reviews_lyft_f1.json') as emoji_unicode:    
    data1 = json.load(emoji_unicode)

with open('rating_lyft_new.json') as emoji_unicode:    
    data2 = json.load(emoji_unicode)


for i in range(1,len(data2.keys())+1):
	# print data2[str(i)]
	# if len(data2[str(i)]['5_star']) == 0:
	# 	continue
	try:
		DAY[data2[str(i)]['date']]=dict()
	except:
		continue
	DAY[data2[str(i)]['date']]['1_star']=data2[str(i)]['1_star']
	DAY[data2[str(i)]['date']]['2_star']=data2[str(i)]['2_star']
	DAY[data2[str(i)]['date']]['3_star']=data2[str(i)]['3_star']
	DAY[data2[str(i)]['date']]['4_star']=data2[str(i)]['4_star']
	DAY[data2[str(i)]['date']]['5_star']=data2[str(i)]['5_star']
print "day dict created"

count=1
for i in range(1,len(data1.keys())+1):
	# print data1[str(i)]['review_date']
	if data1[str(i)]['review_date'][0] == '0':
		data1[str(i)]['review_date']=data1[str(i)]['review_date'][1:]
	try:
		FEATURE[str(i)]=dict()
		FEATURE[str(i)]['rating']=data1[str(i)]['rating']
		
		FEATURE[str(i)]['body_score']=data1[str(i)]['body_score']
		FEATURE[str(i)]['title_score']=data1[str(i)]['title_score']
		FEATURE[str(i)]['word_count']=len(preprocess(data1[str(i)]['review_body']))
		FEATURE[str(i)]['text']=preprocess(data1[str(i)]['review_body'])
		FEATURE[str(i)]['1_star']=DAY[data1[str(i)]['review_date']]['1_star']
		FEATURE[str(i)]['2_star']=DAY[data1[str(i)]['review_date']]['2_star']
		FEATURE[str(i)]['3_star']=DAY[data1[str(i)]['review_date']]['3_star']
		FEATURE[str(i)]['4_star']=DAY[data1[str(i)]['review_date']]['4_star']
		FEATURE[str(i)]['5_star']=DAY[data1[str(i)]['review_date']]['5_star']

		# print "for " +str(i)+" \t"+str(len(FEATURE[str(i)].keys()))
		# print FEATURE[str(i)]
		# if len(FEATURE[str(i)].keys()) == 4:
		# 	FEATURE.pop(str(i),None)
		# 	print " no date info for : " +str(i)
		# else:
		# 	print "done for "+str(i)
	except Exception as e:
		# print data1[str(i)]['review_date']
		# print e
		count+=1
		continue

print "Full data created"
for i in range(1,len(FEATURE.keys())+1):
	if len(FEATURE[str(i)].keys()) < 9:
		# print FEATURE[str(i)]
		FEATURE.pop(str(i),None)
		# print " no date info for ?: " +str(i)
print "incomplete records removed"

editDataSet()


with open ('feature_lyft.json','w') as fp:
	json.dump(NORM_FEATURE,fp)


with open('feature_lyft.json', 'rb') as f_in, gzip.open('feature_lyft.json.gz', 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)