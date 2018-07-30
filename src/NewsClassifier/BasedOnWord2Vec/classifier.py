import math
import json
import os

DOC_NUM=1883719
idf= {}
vec={}

class word_info:
	def __init__(self, word, tfidf):
		self.word = word
		self.tfidf = tfidf

def get_top_tfidf(content,topn=10):
	line = content.strip().lower().split()
	words = [word for word in line if word.isalpha()]
	word_count = {}
	word_num=0
	for w in words:
                word_num = word_num + 1
		if not word_count.has_key(w):
                        word_count[w] = 0
		word_count[w] = word_count[w] + 1
	word_list = []
	for w in word_count:
		if idf.has_key(w):
			tfidf = word_count[w] *1.0 / word_num * idf[w]
			word_list.append(word_info(w,tfidf))
	word_list.sort(key = lambda x : x.tfidf, reverse = True)
	result = []
	for w in word_list:
		if len(result)>=topn:
			break
		result.append(w)
		#print(w.word + '\t' + str(w.tfidf))
	return result

def getVec(line):
	line = line[1:-2]
	a = line.split(',')
	a = [float(w) for w in a]
	return a

def cosSimilar(a,b):
	n = len(a)
	if n!=len(b):
		return 0
	m=0
	am=0
	bm=0
	for i in range(0,n):
		m = m + (a[i]*b[i])
		am = am + (a[i]*a[i])
		bm = bm + (b[i]*b[i])
	return m / (math.sqrt(am*bm))		

if __name__ == '__main__':
	corpList = ['google','amazon','microsoft','nvdia','apple','alibaba','walmart','starbucks']
	word_file = 'word_info.txt'
        file_object = open(word_file)
	for line in file_object:
		data = line.split('\t')
		word_doc_count = int(data[1])
		idf[data[0]] = math.log(DOC_NUM*1.0 / word_doc_count)
		vec[data[0]] = getVec(data[2]) 
	#topW = get_top_tfidf("hello microsoft microsoft microsoft  google") 
	#print(str(topW))
	corpList = ['microsoft','google','amazon','alibaba']
	#for c in corpList:
	#	print(c + '\n')
	#	for w in topW:
	#		print(w.word + '\t' + str(w.tfidf*(cosSimilar(vec[c],vec[w.word]))))
	data_folder = '/home/zezhou/workspace/hackathon/data/'
	article_file = data_folder + 'Article_withDate'
	article_data = open(article_file)
	output_data = {}
	result_num = 0
	for line in article_data:
		line_split = line.split('\t')
		url = line_split[0]
		publish_time = line_split[1]
		(date,t) = publish_time.split(' ')
		hour = t.split(':')[0]
		date = date + '_' + hour
		title = line_split[2]
		content = line_split[3]
		topWords = get_top_tfidf(content)
		for corp in corpList:
			corpVec = vec[corp]
			score = 0
			for w in topWords:
				cSimilar = cosSimilar(vec[w.word],corpVec)
				if cSimilar>0.5:
					score = score + w.tfidf * cSimilar
			if (score>0.1):
				key = corp +'/' + date
				#print(corp + '\t' + line)
				if not output_data.has_key(key):
					output_data[key] = []
				output_data[key].append(line)
		#print(line)
		#for w in topWords:
		#	print(w.word + '\t' + str(w.tfidf) + '\n')
		#result_num = result_num + 1
		#if (result_num > 1000):
		#	break;
	for corp_date in output_data:
		output_line = output_data[corp_date]
		(corp,date) = corp_date.split('/')
		foutFolder = data_folder + 'classifier/' + corp
		isExists = os.path.exists(foutFolder)
		if not isExists:
			os.makedirs(foutFolder)
		foutPath = foutFolder + '/' + date
		f = open(foutPath, 'w')
		f.writelines(output_line)
		f.close()
		 
