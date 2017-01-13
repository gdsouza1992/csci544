
import os
import sys


from collections import defaultdict

class BayesData:

    # KEY=WORD : VALUE=[FREQUENCY,HAM,SPAM,P(Word|HAM),P(Word|SPAM)]
    # wordTable = defaultdict(lambda : [0,0,0,0,0])
    # Add-one smoothing
    wordTable = defaultdict(lambda : [0,1,1,0,0])
    totalSpamDocs = 0
    totalHamDocs = 0
    totalSpamWords= 0
    totalHamWords = 0


    def stripWords(self,inputFile,docType):
        docWordCount = 0
        incrementIndex = -1
        if 'HAM' in docType:
            self.totalHamDocs += 1
            incrementIndex = 1

        elif 'SPAM' in docType:
            self.totalSpamDocs += 1
            incrementIndex = 2

        # for word in inputFile.read().replace('\n', ' ').split(" "):
        for word in inputFile.read().split():
            docWordCount += 1
            self.wordTable[word][0] += 1
            self.wordTable[word][incrementIndex] += 1

        if 'HAM' in docType:
            # No Add-one smoothing
            # self.totalHamWords += docWordCount
            # Add-one smoothing
            self.totalHamWords += (2*docWordCount)
        elif 'SPAM' in docType:
            # No Add-one smoothing
            # self.totalSpamWords += docWordCount
            # Add-one smoothing
            self.totalSpamWords += (2*docWordCount)


    def list_files(self,startpath):
        for root, dirs, files in os.walk(startpath):
            print(root)
            beg = root.find('/',len(root)-5)
            end = len(root)

            docType = root[beg+1:end].upper()

            for f in files:
                if ".DS_Store" not in f:
                    fullPathString = ('{}/{}'.format(root,f))
                    file = open(fullPathString, "r",encoding="latin1")
                    self.stripWords(file,docType)

        # count(pharmacy,Spam): number  of times the word pharmacy appears in documents class Spam
        # count(w, Spam): total number of words in documents class Spam


        #Calculate and update P(Word|HAM),P(Word|SPAM)


        for words in self.wordTable.keys():
            if(self.totalHamWords != 0):
                self.wordTable[words][3] = self.wordTable[words][1] / self.totalHamWords
            else:
                self.wordTable[words][3] = 0.0
            if (self.totalSpamWords != 0):
                self.wordTable[words][4] = self.wordTable[words][2] / self.totalSpamWords
            else:
                self.wordTable[words][3] = 0.0





class Helper:

    def writeDictToFile(self,bayesModel):
        spamCount = bayesModel.totalSpamDocs
        hamCount = bayesModel.totalHamDocs

        with open('nbmodel.txt', 'w') as fileWriter:

            fileWriter.write('HAM_DOCS = {}\n'.format(hamCount))
            fileWriter.write('HAM_WORDS = {}\n'.format(bayesModel.totalHamWords))
            fileWriter.write('P(HAM) = {}\n'.format(hamCount / (spamCount + hamCount)))

            fileWriter.write('SPAM_DOCS = {}\n'.format(spamCount))
            fileWriter.write('SPAM_WORDS = {}\n'.format(bayesModel.totalSpamWords))
            fileWriter.write('P(SPAM) = {}\n'.format(spamCount / (spamCount + hamCount)))

            fileWriter.write('*****\n')

            for dictItem in bayesModel.wordTable.items():
                # Store in format HAM,SPAM,Word
                fileWriter.write('{:.10f},{:.10f}@-:-@{}\n'.format(dictItem[1][3],dictItem[1][4],dictItem[0]))



# Main module/function
if __name__ == '__main__':
    bayesData = BayesData()
    bayesData.list_files(sys.argv[1])
    Helper().writeDictToFile(bayesData)
    print('done')
    print(len(bayesData.wordTable))
