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

    actualSpam = 0
    actualHam = 0
    correctlyIdentifiedSpam = 0
    correctlyIdentifiedHam = 0
    wronglyIdentifiedHam = 0
    wronglyIdentifiedSpam = 0
    totalDocs = 0


    def stripWords(self,inputFile,fileWriter):

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
            # print("SPAM ->",inputFile.name)
            fileWriter.write('spam {}\n'.format(inputFile.name))
            if('spam.txt' in inputFile.name):
                self.correctlyIdentifiedSpam += 1
            if ('ham.txt' in inputFile.name):
                self.wronglyIdentifiedSpam += 1

        else:
            # print("HAM ->",inputFile.name)
            fileWriter.write('ham {}\n'.format(inputFile.name))
            if ('ham.txt' in inputFile.name):
                self.correctlyIdentifiedHam += 1
            if ('spam.txt' in inputFile.name):
                self.wronglyIdentifiedHam += 1

        if ('spam.txt' in inputFile.name):
            self.actualSpam += 1
        elif ('ham.txt' in inputFile.name):
            self.actualHam +=1



    def readFromFile(self):


        with open('nbmodel.txt', 'r') as f:
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
                self.wordTable[rowKey][0] = math.log(float(rowValue.split(",")[0]))
                self.wordTable[rowKey][1] = math.log(float(rowValue.split(",")[1]))

    def readNewDoc(self,inputpath,fileWriter):
        for root, dirs, files in os.walk(inputpath):
            # print(root)
            # beg = root.find('/', len(root) - 5)
            # end = len(root)

            # docType = root[beg + 1:end].upper()

            for f in files:
                if ".DS_Store" not in f:
                    fullPathString = ('{}/{}'.format(root, f))
                    file = open(fullPathString, "r", encoding="latin1")
                    self.stripWords(file,fileWriter)







# Main module/function
if __name__ == '__main__':
    classify = Classify()
    classify.readFromFile()
    with open('nboutput.txt', 'w') as fileWriter:
        classify.readNewDoc(sys.argv[1],fileWriter)

    hamAccuracy =0
    spamAccuracy =0


    precisionSpam = classify.correctlyIdentifiedSpam/(classify.correctlyIdentifiedSpam + classify.wronglyIdentifiedSpam)
    recallSpam = classify.correctlyIdentifiedSpam/classify.actualSpam
    f1Spam = (2*precisionSpam*recallSpam)/(precisionSpam + recallSpam)

    print("SPAM Precision =",precisionSpam)
    print("SPAM Recall =",recallSpam)
    print("SPAM F1 Score =",f1Spam)

    precisionHam = classify.correctlyIdentifiedHam/(classify.correctlyIdentifiedHam + classify.wronglyIdentifiedHam)
    recallHam = classify.correctlyIdentifiedHam/classify.actualHam
    f1Ham = (2 * precisionHam * recallHam) / (precisionHam + recallHam)

    print("HAM Precision =",precisionHam)
    print("HAM Recall =",recallHam)
    print("HAM F1 Score =",f1Ham)

    # bayesData = BayesData()
    # bayesData.list_files(sys.argv[1])
    # Helper().writeDictToFile(bayesData)

