import random
import sys
import os
import io


from collections import defaultdict

class Perceptron:

    # KEY=WORD : VALUE=[WEIGHT]
    weightTable = defaultdict(lambda : [0])
    # SET rather than dict as we only need the collection and shuffle it
    fileList = dict()

    bias = 0
    maxIter = 20

    def typeToNumber(self,docType):
        if 'HAM' in docType:
            return -1
        elif 'SPAM' in docType:
            return 1

    def stripWords(self, inputFile, docType,fullPathString):

        wordSetPerFile = set()
        for word in inputFile.read().split():
            self.weightTable[word][0] = 0
            wordSetPerFile.add(word)

        self.fileList[fullPathString] = [self.typeToNumber(docType),wordSetPerFile]







    def list_files(self, startpath):
        for root, dirs, files in os.walk(startpath):
            print(root)
            beg = root.find('/', len(root) - 5)
            end = len(root)

            docType = root[beg + 1:end].upper()

            for f in files:
                if ".DS_Store" not in f and ".txt" in f:
                    fullPathString = ('{}/{}'.format(root, f))
                    file = open(fullPathString, "r", encoding="latin1")
                    self.stripWords(file, docType,fullPathString)

    def doIteration(self):
        keyList = list()
        for eachKey in self.fileList.keys():
            keyList.append(eachKey)

        for i in range(self.maxIter):
            random.shuffle(keyList)

            for eachFile in keyList:

                alpha = 0

                for features in self.fileList[eachFile][1]:
                    # summation fiwi
                    alpha += self.weightTable[features][0]
                #add the bias
                alpha += self.bias

                #claculate y*alpha where y=1 for SPAM and y=-1 for HAM
                y = self.fileList[eachFile][0]
                alpha = alpha * y

                #activation function (step function)
                if(alpha <= 0):
                    # wd = wd + yxd, for all d = 1…D
                    for features in self.fileList[eachFile][1]:
                        self.weightTable[features][0] += y

                    self.bias += y

# Main module/function
if __name__ == '__main__':
    perceptron = Perceptron()
    perceptron.list_files(sys.argv[1])
    perceptron.doIteration()

    with open('nb_model.txt', 'w',encoding="latin1") as f:
        for dictItem in perceptron.weightTable.items():
            #     # Store in format WORD @-:-@ WEIGHT
            f.write('{} {}\n'.format(dictItem[0], dictItem[1]))
        f.close()

    print('done')
    #
    # file = open("newfile.txt", "w")
    #
    # file.write("hello world in the new file")
    #
    # file.write("and another line")

    f.close()
