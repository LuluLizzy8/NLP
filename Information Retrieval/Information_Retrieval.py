import string
import nltk
import math

nltk.download('punkt')

from stop_list import closed_class_stop_words

def parseDocument(fileName, type): 
    with open(fileName, "r") as file:
        rawDoc = file.read()

    rawAbstracts = rawDoc.split(".I ")[1:] #list of all abstracts
    parsedAbstracts = []
    count = 1

    #add all parsed abstracts to list
    for i in rawAbstracts: 
        if type == "query": #added mappedId for query input
            abstract = parseAbstract(i)
            abstract.update({"mappedId": count})
            parsedAbstracts.append(abstract)
            count += 1
        else:
            parsedAbstracts.append(parseAbstract(i))
    return parsedAbstracts

#take in raw abstract sections and parse them to only include id and text
def parseAbstract(rawAbstract):
    lines = str(rawAbstract).strip().split("\n") #list of every line in abstract i
    abstractId = lines[0].strip()
    text = ""
    reached = False
    for line in lines:
        if reached:
            text += line.strip() + " "
        if line.startswith(".W"):
            reached = True
    return {"abstractId": abstractId, "text": processText(text.strip())}

#take in string and remove all unwanted characters and words
def processText(text): 
    terms = nltk.word_tokenize(text.lower())
    return [word for word in terms if word not in closed_class_stop_words and word not in string.punctuation and not word.isdigit()]

def calculateIDF(abstracts):
    totalAbstracts = 0
    idf = {}
    for abstract in abstracts:
        setAbstract = set(abstract["text"])
        totalAbstracts += 1
        for term in setAbstract:
            if term not in idf.keys():
                idf[term] = 0
            idf[term] += 1
    
    for term in idf.keys():
        idf[term] = math.log((totalAbstracts)/(idf[term]))

    return idf

#adds "vector" to each abstract dictionary
#vector is a dictionary of each term's TFIDF
def calculateTFIDF(abstracts, idf):
    for abstract in abstracts:
        vector = {}
        termFrequency = {}
        #get term frequencies
        for term in abstract["text"]:
            termFrequency[term] = termFrequency.get(term, 0) + 1
        #calculate vectors for each term
        for term in termFrequency.keys():
            if term not in idf.keys():
                vector[term] = 0
            else:
                vector[term] = (termFrequency[term]) * idf[term]
        abstract.update({"vector": vector})

def calculateCosineSimilarity(query, abstract):
    numerator = 0
    denominatorA = 0
    denominatorB = 0
    for term in query["text"]:
        denominatorA += query["vector"][term] ** 2
        if term in abstract["text"]:
            numerator += query["vector"][term] * abstract["vector"][term]

    for term in abstract["text"]:
        denominatorB += abstract["vector"][term] ** 2

    if denominatorA == 0 or denominatorB == 0:
        return 0
    return numerator / ((denominatorA * denominatorB) ** 0.5)

def main():
    abstracts = parseDocument("cran.all.1400", "notquery")
    #"abstracts" is list of abstracts
        #contains "abstractId": .I
        #         "text": list of all wanted terms
        #         "vector": dictionary of all terms and their TFIDF
    queries = parseDocument("cran.qry", "query")
    #"queries" is a list of queries
        #contains "abstractId": .I
        #         "text": list of all wanted terms
        #         "mappedId": list of all wanted terms
        #         "vector": dictionary of all terms and their TFIDF
    idf = calculateIDF(abstracts)
    calculateTFIDF(abstracts, idf)
    calculateTFIDF(queries, idf)

    with open("output.txt", "w") as output:
        for query in queries:
            results = []
            for abstract in abstracts:
                cosineSimilarity = calculateCosineSimilarity(query, abstract)
                if cosineSimilarity > 0:
                    results.append((abstract["abstractId"], cosineSimilarity))

            #sort results by cosineSimilarity
            results.sort(key=lambda tup: tup[1], reverse = True)
            
            top_results = results[:100]
            if len(top_results) < 100 or all(res[1] == 0 for res in top_results):
                # If fewer than 100 results or all results have zero similarity, fill in with zero scores
                top_results += [(doc['abstractId'], 0) for doc in abstracts[len(top_results):100]]
            # if len(results) < 100:
            #     results += [(1, 0)] * (100 - len(results))
            for abstractId, cosineSimilarity in top_results:
                output.write(f"{query['mappedId']} {abstractId} {cosineSimilarity}\n")

main()