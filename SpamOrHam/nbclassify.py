import os
import sys
import math


from collections import defaultdict

# class BayesData:
#
#     # KEY=WORD : VALUE=[FREQUENCY,HAM,SPAM,P(Word|HAM),P(Word|SPAM)]
#     wordTable = defaultdict(lambda : [0,0,0,0,0])
#     totalSpamDocs = 0
#     totalHamDocs = 0
#     totalSpamWords= 0
#     totalHamWords = 0
#
#
#     def stripWords(self,inputFile,docType):
#         docWordCount = 0
#         incrementIndex = -1
#         if 'HAM' in docType:
#             self.totalHamDocs += 1
#             incrementIndex = 1
#
#         elif 'SPAM' in docType:
#             self.totalSpamDocs += 1
#             incrementIndex = 2
#
#         for word in inputFile.read().replace('\n', ' ').split(" "):
#             docWordCount += 1
#             self.wordTable[word][0] += 1
#             self.wordTable[word][incrementIndex] += 1
#
#         if 'HAM' in docType:
#             self.totalHamWords += docWordCount
#         elif 'SPAM' in docType:
#             self.totalSpamWords += docWordCount
#







class Classify:
    spamPrior = 0
    hamPrior = 0
    wordTable = defaultdict(lambda: [0, 0])

    resultTable = list()
    identifiedSpam = 0
    actualSpam = 0
    identifiedHam = 0
    actualHam = 0
    totalDocs = 0


    def stripWords(self,inputFile):

        #METRICS
        self.totalDocs += 1

        totHam = 0.0
        totSpam = 0.0


        # Cumulative summation counters
        if(self.hamPrior != 0):
            totHam = math.log(self.hamPrior)
        if(self.spamPrior != 0):
            totSpam = math.log(self.spamPrior)

        # for word in inputFile.read().replace('\n', ' ').split(" "):
        for word in inputFile.read().split():

            wordProb = self.wordTable[word]
            # WordProb[0] -> Log of Ham Probability
            # WordProb[1] -> Log of Spam Probability
            totHam += wordProb[0]
            totSpam += wordProb[1]



        if(totSpam > totHam):
            print("SPAM ->",inputFile.name,)
            if('spam.txt' in inputFile.name):
                self.identifiedSpam += 1

        else:
            print("HAM ->",inputFile.name)
            if ('ham.txt' in inputFile.name):
                self.identifiedHam += 1

        if ('spam.txt' in inputFile.name):
            self.actualSpam += 1
        elif ('ham.txt' in inputFile.name):
            self.actualHam +=1



    def readFromFile(self):


        with open('model_data.txt', 'r') as f:
            fileLines = f.read().splitlines()

        modelInfo = fileLines[:6]
        self.hamPrior = float(modelInfo[2].split(' = ')[1])
        self.spamPrior = float(modelInfo[5].split(' = ')[1])

        modelValues = fileLines[7:]

        for rowData in modelValues:
            if len(rowData.split("@-:-@")) == 1:
                continue
            else:
                rowKey = rowData.split("@-:-@")[1]
                rowValue = rowData.split("@-:-@")[0]
                self.wordTable[rowKey][0] = 0.0 if float(rowValue.split(",")[0]) == 0 else (math.log(float(rowValue.split(",")[0])))
                self.wordTable[rowKey][1] = 0.0 if float(rowValue.split(",")[1]) == 0 else (math.log(float(rowValue.split(",")[1])))

    def readNewDoc(self,inputpath):
        for root, dirs, files in os.walk(inputpath):
            # print(root)
            # beg = root.find('/', len(root) - 5)
            # end = len(root)

            # docType = root[beg + 1:end].upper()

            for f in files:
                if ".DS_Store" not in f:
                    fullPathString = ('{}/{}'.format(root, f))
                    file = open(fullPathString, "r", encoding="latin1")
                    self.stripWords(file)







# Main module/function
if __name__ == '__main__':
    classify = Classify()
    classify.readFromFile()
    classify.readNewDoc(sys.argv[1])

    hamAccuracy =0
    spamAccuracy =0

    if(classify.actualSpam != 0):
        spamAccuracy = classify.identifiedSpam/classify.actualSpam
    if (classify.actualHam != 0):
        hamAccuracy = classify.identifiedHam/classify.actualHam

    print("SPAM Accuracy =", spamAccuracy*100)
    print("HAM Accuracy=", hamAccuracy*100)

    # bayesData = BayesData()
    # bayesData.list_files(sys.argv[1])
    # Helper().writeDictToFile(bayesData)

