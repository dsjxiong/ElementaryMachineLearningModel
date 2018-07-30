import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

sid = SentimentIntensityAnalyzer()

def sentence_result(sentence):
	ss = sid.polarity_scores(sentence)
	r = []
	for k in ss:
		r.append(ss[k])
	return r[3]

def document_result(doc):
	sentence_list = re.split(r"[.,!,?,;]",doc)
	score = 0
	sentence_num = 0
	for sentence in sentence_list:
		if len(sentence)<3:
			continue
		sentence_score = sentence_result(sentence)
		sentence_num = sentence_num + 1
		score = score + sentence_score
	return score * 1.0 / sentence_num

def local_test():
	while True:
		sentence = raw_input()
		print(document_result(sentence))

if __name__ == '__main__':
	classifierFolder = '/data/zezhou/workspace/hackathon/data/classifier/'
	resultFolder = '/data/zezhou/workspace/hackathon/data/sentiment_result/'
	for corpName in os.listdir(classifierFolder):
		corpFolder = classifierFolder + corpName
		sentimentResult = {}
	#	num = 0
		for dateStr in os.listdir(corpFolder):
			articleFilePath = corpFolder + '/' + dateStr
			articleFile = open(articleFilePath,'r')
			articleList = articleFile.readlines()
			dailyResult = 0
			#num = num + 1
			#if num == 10:
			#	break
			count = 0
			for article in articleList:
				count = count + 1
				articleResult = document_result(article)
				dailyResult = dailyResult + articleResult
			sentimentResult[dateStr] = dailyResult*1.0 / count
		outputFilePath = resultFolder + corpName + '.txt'
		outputFile = open(outputFilePath, 'w')
		outputList = []
		for key in sentimentResult.keys():
			outputList.append(key + '\t' + str(sentimentResult[key]) + '\n')
		print(outputFilePath)
		outputFile.writelines(outputList)	
