import sys
import os
import re
from nltk.corpus import stopwords
from nltk.stem.porter import *
import string
import operator
import math
from rouge import Rouge



hypothesis=sys.argv[2]
documents=sys.argv[1]
threshold=sys.argv[4]
reference=sys.argv[3]

print("please wait your program is running!!!")
fp_write=open(hypothesis,"w")
stop = set(stopwords.words('english'))
stemmer = PorterStemmer()
docs_lines_striped=[]
original_line_list=[]
for filename in os.listdir(documents):
	#print(filename)
	fp=open(documents+filename,"r")
	lines=fp.readlines()
	lines_striped=[]
	#cleanr = re.compile('<.*?>')
	cleanr = re.compile('<[^>]+>')
	for line in lines:
		#line=line.strip()
		line=re.sub(cleanr, '', line)
		if line!='':
			original_line_list.append(line)
		line=line.strip()
		line_list=[i for i in line.lower().split() if i not in stop]
		'''
		pine=' '.join(line_list)
		if pine!='':
			original_line_list.append(line)
		'''
		line_list=[stemmer.stem(line_list_i) for line_list_i in line_list]
		
		line=' '.join(line_list)
		#line.translate(None, string.punctuation)
		exclude = set(string.punctuation)
		line = ''.join(ch for ch in line if ch not in exclude)
		if line!='':
			lines_striped.append(line)

	#print(lines_striped)
	#print(lines_striped[3])
	docs_lines_striped.append(lines_striped)


#print(docs_lines_striped)


inverted_index={}

for docs in docs_lines_striped:
	for sentence in docs:
		sentence_list=[i for i in sentence.split()]
		for word in sentence_list:
			if word in inverted_index:
				inverted_index[word]=inverted_index[word]+1
			else:
				inverted_index[word]=1

#print(inverted_index)
'''
count=0
for key,value in sorted(inverted_index.iteritems()):
	count=count+1

print(count)
'''

#sorted_x = sorted(inverted_index.items(), key=operator.itemgetter(0))
#print(sorted_x)
N=0
for sub_list in docs_lines_striped:
	for line in sub_list:
		N=N+1

#print(N)
#print(len(original_line_list))
N_inverted_index={}
for sub_list in docs_lines_striped:
	for line in sub_list:
		line_list=line.split()
		for key in inverted_index:
			if key in line_list:
				if key in N_inverted_index:
					N_inverted_index[key]=N_inverted_index[key]+1
				else:
					N_inverted_index[key]=1


#print(N_inverted_index)

idf={}

for key in N_inverted_index:
	x=N/N_inverted_index[key]
	idf[key]=math.log(x,10)
'''
for key,value in idf.iteritems():
	print(key,value)
'''

#now solve idf modified cosine

combine_all_sub_lists=[]

for sub_list in docs_lines_striped:
	for line in sub_list:
		combine_all_sub_lists.append(line)

#print(combine_all_sub_lists)

dict_list_idf={}
for i in range(len(combine_all_sub_lists)):
	list_idf=[]
	for j in range(len(combine_all_sub_lists)):
		if i==j:
			idf_modified_cosine=1.0
			list_idf.append(idf_modified_cosine)
		else:
			line1=combine_all_sub_lists[i]
			line2=combine_all_sub_lists[j]
			x=line1.split()
			y=line2.split()
			numerator=0.0
			word_checked=[]
			for sub in x:
				if sub in y and sub not in word_checked:
					word_checked.append(sub)
					if sub in idf:
						numerator=numerator+x.count(sub)*y.count(sub)*math.pow(idf[sub],2)

			word_checked_x=[]
			denominator1=0.0
			for sub in x:
				if sub not in word_checked_x:
					word_checked_x.append(sub)
					denominator1=denominator1+math.pow((x.count(sub)*idf[sub]),2)
			denominator1=math.sqrt(denominator1)
			
			word_checked_y=[]
			denominator2=0.0
			for sub in y:
				if sub not in word_checked_y:
					word_checked_y.append(sub)
					denominator2=denominator2+math.pow((y.count(sub)*idf[sub]),2)
			denominator2=math.sqrt(denominator2)

			denominator=denominator1*denominator2

			idf_modified_cosine=numerator/denominator
			if idf_modified_cosine<float(threshold):
				list_idf.append(float(0.0))
			else:
				list_idf.append(idf_modified_cosine)

	dict_list_idf[i]=list_idf


#print(dict_list_idf)

degree_of_each_line={}
for key in dict_list_idf:
	k=dict_list_idf[key].count(0.0)
	degree_of_each_line[key]=N-k-1

#print(degree_of_each_line)
'''
for i in range(250):
	max(degree_of_each_line.iteritems(), key=operator.itemgetter(1))[0]
'''

#k=max(degree_of_each_line.iteritems(), key=operator.itemgetter(1))[0]
#print(k,degree_of_each_line[k])
no_of_words=0
for i in range(250):
	k=max(degree_of_each_line.iteritems(), key=operator.itemgetter(1))[0]
	no_list=original_line_list[k].split()
	if no_of_words+len(no_list)<=250:
		fp_write.write(original_line_list[k])
		no_of_words=no_of_words+len(no_list)
	else:
		break

	for j in range(len(dict_list_idf[k])):
		if dict_list_idf[k][j]>float(threshold) and k!=j:
			if j in dict_list_idf:
				del dict_list_idf[j]
			degree_of_each_line[j]=0
	if k in dict_list_idf:
		del dict_list_idf[k]
	degree_of_each_line[k]=0

print("summary written to file: ",hypothesis)

print("waiting for rouge scores!!!")

fp_write.close()


fp_hypo=open(hypothesis,"r")
fp_ref=open(reference,"r")


lines_hypo=fp_hypo.read()
lines_ref=fp_ref.read()

rook=Rouge()

scores = rook.get_scores(lines_hypo, lines_ref)
print(scores)

