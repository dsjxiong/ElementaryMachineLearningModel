from gensim.models import Word2Vec
import sys

class MySentence(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
 		file_object = open(self.dirname,'r')#, encoding='UTF-8')
 		for line in file_object:
 			rline = line.strip().lower().split()
 			word_line = [word for word in rline if word.isalpha()]
 			yield word_line

class w2v_result(object):
	def __init__(self, fname = '/home/zezhou/workspace/hackathon/Word2Vec/wordembedding'):
		self.w2v_model = Word2Vec.load(fname)

	def most_similar(self, word, top_n=50):
		return self.w2v_model.most_similar(word, topn = top_n)

	def get_vector(self, word):
		print(word)
		return self.w2v_model[word]

	def similarity(self, word1, word2):
		return self.w2v_model.similarity(word1, word2)		

if __name__ == '__main__':
        #sentences = MySentence("/home/zezhou/workspace/hackathon/data/ArticleDescription.tsv")
        #model = Word2Vec(sentences, sg=1, size=128,  window=5,  min_count=10,  negative=3, sample=0.001, hs=1, workers=4)
        #model.save(fname)
        #model = Word2Vec.load(fname)
        m = w2v_result()
        print(m.most_similar(sys.argv[1]))
	#print(m.similarity(sys.argv[1],sys.argv[2]))
