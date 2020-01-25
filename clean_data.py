import nltk
import json
import fuzzy
from stemming.porter2 import stem
from sets import Set
import editdistance

flags=Set([])
sound_vocab=dict()
map_vocab=dict()
dict1=dict()
dict2=dict()
train_pos=[]
train_neg=[]
test_pos=[]
test_neg=[]
train_mid=[]
test_mid=[]
review_vocab=[]
## globals
def buildVocabDict():
	global dict1
	global dict2

	text_file = open("dict1.txt", "r")
	lines = text_file.readlines()
	for line in lines:
		items=line.split('\t')
		key=items[0]
		value=items[1]
		value=items[1][:len(value)-1]
		dict1[key]=value
	text_file.close()

	text_file = open("dict2.txt", "r")
	lines = text_file.readlines()
	for line in lines:
		items=line.split('|')
		if len(items)>2:
			continue
		key=items[0].split('\t')[1]
		item=items[1]
		item=item[:len(item)-1]
		# print key+" :: "+item
	text_file.close()	

def getCloseSound(words,flag):
	distance=[]

	for word in words:
		distance.append(editdistance.eval(word,flag))
	
	min_index=0
	for i in range(0,len(distance)):
		if(distance[min_index]>distance[i]):
			min_index=i
	
	return words[min_index]

def checkSoundexMatch():
	global flags
	global sound_vocab
	global map_vocab

	count=1
	soundex=fuzzy.Soundex(6)
	for flag in flags:
		sound=soundex(flag)
		if sound in sound_vocab:
		 	map_vocab[flag]=getCloseSound(sound_vocab[sound],flag)
		 	# print "match for - "+flag+" :: "+map_vocab[flag]
		 	# flags.discard(flag)
		 	# print "sound match no :"+str(count)
		 	count+=1

def buildSoundex():
	global sound_vocab
	english_vocab = set(w.lower() for w in nltk.corpus.words.words())
	soundex=fuzzy.Soundex(6)
	for word in english_vocab:
		sound=soundex(word)
		if sound in sound_vocab:
			# print "Soundex map collision found "
			sound_vocab[sound].append(word)
		else:
			sound_vocab[sound]=[word]

def checkVocab(data):
	global flags
	global dict1
	global dict2
	global review_vocab
	english_vocab = set(w.lower() for w in nltk.corpus.words.words())
	match_count = 0
	for key in data.keys():
		# print data[key]
		text=data[key]['text']



		for i in range(0,len(text)):

		
			if not text[i] in english_vocab:

				if stem(text[i]) in dict1:
					text[i]=dict1[stem(text[i])]
					# print "stem match for :: "+stem(text[i])
					match_count+=1

				elif stem(text[i]) in dict2:
					text[i]=dict2[stem(text[i])]
					# print "stem match for :: "+stem(text[i])
					match_count+=1

				elif text[i] in dict1:
					text[i]=dict1[text[i]]
					# print "match for :: "+text[i]
					match_count+=1

				elif text[i] in dict2:
					text[i]=dict2[text[i]]
					# print "match for :: "+text[i]
					match_count+=1

				
				else:
					flags.add(text[i])
				# print text[i]
			review_vocab.append(text[i])

	print "total out of vocab words:"+str(len(flags))
	print "total online dict matches :"+str(match_count)
	print "Total size of review dictionary : "+str(len(review_vocab))

def removeNoise(data):
	global flags
	global map_vocab

	for key in data.keys():
		text=data[key]['text']

		for i in range(0,len(text)):
			if text[i] in map_vocab:
				data[key]['text'][i]=map_vocab[text[i]]	
				# print "Soundex changed for :: " +text[i]			
			
def doStem(data):
	for key in data.keys():
		text=data[key]['text']

		for i in range(0,len(text)):
			try:
				text[i]=stem(text[i])
			except Exception:
				print "error for word ::"+str(text[i])

def printDict(data):
	for key in data.keys():
		print key+" :: "+data[key]
	print "total length of soundex map :"+str(len(data.keys()))

def splitData(data_final,train_set,test_set):
	count=int(0.66*len(data_final))
	for i in range(0,count):
		train_set.append(data_final[i])
	for i in range(count,len(data_final)):
		test_set.append(data_final[i])

def writeJSONFile():
	data=dict()
	global train_pos
	global train_neg
	global test_pos
	global test_neg	
	global train_mid
	global test_mid
	data['train_pos']=train_pos
	data['train_neg']=train_neg
	data['test_pos']=test_pos
	data['test_neg']=test_neg
	data['train_mid']=train_mid
	data['test_mid']=test_mid
	with open ('lstm_data.json','w') as fp:
		json.dump(data,fp)

def storeDeepData(data):
	pos=[]
	neg=[]
	mid=[]
	global train_pos
	global train_neg
	global test_pos
	global test_neg
	global train_mid
	global test_mid
	for key in data.keys():
		if data[key]['rating'] == '4' or data[key]['rating'] == '5' :
			pos.append(data[key])
		elif data[key]['rating'] == '1' or data[key]['rating'] == '2' :
			neg.append(data[key])
		else:
			mid.append(data[key])

	splitData(pos,train_pos,test_pos)
	splitData(neg,train_neg,test_neg)
	splitData(mid,train_mid,test_mid)
	print "len of train pos split :: "+str(len(train_pos))
	print "len of train neg split :: "+str(len(train_neg))
	print "len of test pos split :: "+str(len(test_pos))
	print "len of test neg split :: "+str(len(test_neg))
	print "len of test mid split :: "+str(len(test_mid))

	writeJSONFile()
	
def main():
	global map_vocab
	with open('reviews_flipkart_uber_new.json') as emoji_unicode:
		data = json.load(emoji_unicode)

	# doStem(data) ## stemming 
	# print "Stemming completed ..."

	# for key in data.keys():
	# 	print data[key]['text']
	buildVocabDict()
	print "online dict 1 & 2 created"
	checkVocab(data)
	print "vocab check completed ..."
	buildSoundex()
	print "sound vocab created ..."
	checkSoundexMatch()
	print "sound match done ..."
	removeNoise(data)
	print "All noise removed ..."
	# doStem(data) ## stemming 
	# print "Stemming completed ..."
	storeDeepData(data)
	print "deep learning data stored ..."
	# printDict(map_vocab)
	# print "Length of data :"+str(len(data.keys()))
	with open ('feature_flipkart_norm.json','w') as fp:
		json.dump(data,fp)


if __name__ == '__main__':
	main()


# check with manual dict and replace
# check presence in vocab
# unusual words check for soundex with english & online vocab
# stemming all words
# check with manual dict
# check soundex with ......

