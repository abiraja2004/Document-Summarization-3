# Document-Summarization

Implemented the Degree Centrality and Text Rank algorithms on a number of documents.

Compared both the algorithms using the rouge-1, rouge-2 and rouge-l scores.

It was found that Text Rank performed better than Degree Centrality.

Given below is one of the results that had been obtained.

Topic 3,Degree centrality,Threshold=0.3:
[{'rouge-l': {'p': 0.13675213675213677, 'r': 0.14545454545454545, 'f': 0.14070182461796485}, 'rouge-2': {'p': 0.09251101321585903, 'r': 0.10344827586206896, 'f': 0.09767441362022741}, 'rouge-1': {'p': 0.21301775147928995, 'r': 0.24489795918367346, 'f': 0.22784809629005778}}]

Topic 3,Text Rank,Threshold=0.3:
[{'rouge-l': {'p': 0.1859504132231405, 'r': 0.20454545454545456, 'f': 0.193927693927108}, 'rouge-2': {'p': 0.13617021276595745, 'r': 0.15763546798029557, 'f': 0.14611871648787572}, 'rouge-1': {'p': 0.2802197802197802, 'r': 0.3469387755102041, 'f': 0.3100303901933648}}]

