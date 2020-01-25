import csv
import json
# from sets from Set

train_set=[]
test_set=[]
hi_set=dict()
lo_set=dict()
hi_list=[]
lo_list=[]
hi_word=[]
lo_word=[]

high_word=[]
low_word=[]
####### globals #############


def storeLow(text):
	global lo_set

	for i in text:
		if i not in lo_set:
			lo_set[i]=1
		else:
			lo_set[i]+=1


def storeHigh(text):
	global hi_set

	for i in text:
		if i not in hi_set:
			hi_set[i]=1
		else:
			hi_set[i]+=1

def getWords(val1,val2,val3,val4):
	global train_set
	print "length of train_set:"+str(len(train_set))
	for iter in train_set:
		if iter['rating']==str(val1) or iter['rating']==str(val2):
			storeLow(iter['text'])
		if iter['rating']==str(val3) or iter['rating']==str(val4):
			storeHigh(iter['text'])

def splitData(data_final):
	global train_set
	global test_set

	count=int(0.66*len(data_final))
	for i in range(0,count):
		train_set.append(data_final[i])
	for i in range(count,len(data_final)):
		test_set.append(data_final[i])

def sortData(data_list):
	data_one=[]
	data_two=[]
	data_three=[]
	data_four=[]
	data_five=[]
	data_final=[]
	# print data_list[0]
	for i in range(0,len(data_list)):
		if data_list[i]['rating']=='1':
			data_one.append(data_list[i])
		if data_list[i]['rating']=='2':
			data_two.append(data_list[i])
		if data_list[i]['rating']=='3':
			data_three.append(data_list[i])
		if data_list[i]['rating']=='4':
			data_four.append(data_list[i])
		if data_list[i]['rating']=='5':
			data_five.append(data_list[i])

	print " data_one :"+str(len(data_one))
	print " data_two :"+str(len(data_two))
	print " data_three :"+str(len(data_three))
	print " data_four :"+str(len(data_four))
	print " data_five :"+str(len(data_five))
	
	count=0
	for i in range(0,len(data_one)):
		data_final.append(data_one[count])
		data_final.append(data_two[count])
		data_final.append(data_three[count])
		data_final.append(data_four[count])
		data_final.append(data_five[count])
		count+=1
	return data_final

def serializeData(data):
	data_list=[]
	for i in data.keys():
		data_list.append(data[i])
	return data_list

def readFile(filename):
	with open(filename) as emoji_unicode:
		data = json.load(emoji_unicode)
	return data

def displayData(data_final):
	for i in data_final:
		print i

def  displayDict(data):
	for i in data.keys():
		print i+ " :: " +str(data[i])

def getKey(item):
	return item[1]
def removeCommonWords():
	global hi_set
	global lo_set

	for key1 in hi_set.keys():
		for key2 in lo_set.keys():
			if key1==key2:
				del hi_set[key1]
				del lo_set[key2]

def getSortedList():
	global hi_list
	global lo_list


	for i in hi_set.keys():
		hi_list.append((i,hi_set[i]))
	for i in lo_set.keys():
		lo_list.append((i,lo_set[i]))

	hi_list=sorted(hi_list,key=getKey,reverse=True)
	lo_list=sorted(lo_list,key=getKey,reverse=True)

def getWordRank():
	global hi_word
	global lo_word
	global hi_list
	global lo_list

	# removeCommonWords()
	# displayDict(hi_set)
	getSortedList()
	count=0
	print "length of hi list :: "+str(len(hi_list))
	print "length of lo list :: "+str(len(lo_list))
	print " Top ranked elements are:"
	for i in hi_list:
		print i[0] + " :: "+ str(i[1])
		if len(i[0])==1 or len(i[0])==2:
			continue 
		hi_word.append(i[0])
		count+=1
		if count >= 30 :
			break
	
	count=0
	print "\n \n \n Bottom ranked elements are:"
	for i in lo_list:
		print i[0] + " :: "+ str(i[1])
		if len(i[0])==1 or len(i[0])==2:
			continue 
		lo_word.append(i[0])
		count+=1
		if count >= 30 :
			break
def storeData():
	global hi_word
	global lo_word
	result=dict()
	result['hi']=hi_word
	result['lo']=lo_word
	with open ('word_map.json','w') as fp:
		json.dump(result,fp)

def getFeature(data_final):
	global hi_word
	global lo_word

	for iter in data_final:
		text=iter['text']
		### for top words
		for j in range(0,len(hi_word)):
			temp='h'+str(j+1)
			iter[temp]=0

			for word in text:
				if word==hi_word[j]:
					iter[temp]+=1

		### for bottom words
		for j in range(0,len(lo_word)):
			temp='l'+str(j+1)
			iter[temp]=0

			for word in text:
				if word==hi_word[j]:
					iter[temp]+=1
		del iter['text']
	return data_final

def storeData(data_list):
	keys = data_list[0].keys()
	with open('input.csv', 'wb') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(data_list)

def main():
	global hi_set
	global lo_set

	data=readFile('feature_lyft.json')
	print "file read "
	data_final=serializeData(data)
	print "data serialized"
	############ pre sort ###########
	data_final=sortData(data_final)
	print "data sorted"
	############ post sort ##########
	# displayData(data_final)
	splitData(data_final)
	print "data split done"
	getWords(1,2,4,5)	
	print "both dicts created"	#to get low and high ranking words
	# displayDict(hi_set)
	# print "length is :" +str(len(hi_set))
	getWordRank()
	print "Word rank obtained ..."
	# storeData()
	datafinal=getFeature(data_final)
	print "All features obtained ..."
	# data_final=sortData(data_final)
	# print "Data sorted ..."
	
	storeData(data_final)
	print "Data stored in csv ..."
			
if __name__ == '__main__':
	main()