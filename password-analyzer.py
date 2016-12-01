import math, hashlib
from collections import OrderedDict


class pwa(object):
    def __init__(self):
        self.inpFile = 'passwords-hw4'
        self.passwordTotal = 0
        self.uniquePasswordTotal = 0
        self.alphaTotal = 0
        self.effectiveEntropy = 0
        self.maxEntropy = 0
        self.uniqueEffectiveEntropy = 0
        self.uniqueMaxEntropy = 0
        self.passDic= {}
        self.passFreq = {}
        self.passProb = {}
        self.passHash= {}
        self.passHashAnswers= {}
        self.passRank = {}

    def main(self):
        self.Q1A()
        self.outputQ1() #other questions utilize this loop
        self.Q2_Q3()
        self.Q4()
        self.output()

    def Q1A(self):
        lines = 0
        with open(self.inpFile, 'r') as inp:
            for line in inp:
                line= line.rstrip()
                if line in self.passDic:
                    self.passDic[line] +=1  #count feq of all passwords
                else:
                    self.uniquePasswordTotal +=1    #count unique passwords
                    self.passDic[line] = 1  #count feq of all passwords
                    self.Q1B(line)  #count chars of unique passwords for later questions
                    self.passHash[hashlib.md5(line).hexdigest()] = line
                lines += 1
        self.passwordTotal= lines

    def Q1B(self, line):        #only used inside of function Q1A()
        for x in line:
            if x.isalpha():
                self.alphaTotal += 1
                x= x.upper()
                if x in self.passFreq:
                    self.passFreq[x] +=1
                else:
                    self.passFreq[x] = 1

    def Q2_Q3(self):      #Combines questions Q2A Q2B and Q3A and Q3B
        for x in self.passProb.values():
            if(x != 0):
                self.effectiveEntropy+= x *math.log(x,2) #Q2A
                self.uniqueEffectiveEntropy += (1 / float(self.uniquePasswordTotal)) * math.log((1 / float(self.uniquePasswordTotal)),2)    #Q3A
        self.effectiveEntropy= self.effectiveEntropy*-1 #Q2A
        self.uniqueEffectiveEntropy = self.uniqueEffectiveEntropy * -1    #Q3A
        self.maxEntropy = math.log(self.passwordTotal,2) #Q2B
        self.uniqueMaxEntropy = math.log(self.uniquePasswordTotal,2)  # Q3B

    def Q4(self):
        with open('Q4.txt', 'w') as oup:
            with open("Q4in.txt") as inp:
                tempDictionary = OrderedDict(sorted(self.passRank.items()))
                tempDictionary = sorted(tempDictionary.iteritems(), key=lambda x: x[1], reverse=True)
                tempList = []
                for x in tempDictionary:
                    tempList.extend(x[1])
                for line in inp:
                    line = line.rstrip()
                    # if line in self.passHash:
                    #     oup.write(line +'\t' +self.passHash[line] +'\n')
                    index = 0
                    for passwd in tempList:
                        index+=1
                        if passwd == self.passHash[line]:
                            oup.write(line + '\t' + self.passHash[line] + '\t' + index.__str__() +'\n')

    def outputQ1(self): #made Q1A seperate because other functions use its loop
        with open("Q1A.txt", 'w') as oup:
            for x, y in sorted(self.passDic.items()):
                if y in self.passRank:
                    self.passRank[y].append(x)              #ceep track of rank
                else:
                    self.passRank[y] = [x]
                prob = round(float(self.passDic[x]) / float(self.passwordTotal), 10)
                self.passProb[x] = prob  # make a dict with prob for later qustions
                oup.write(x + "\t" + y.__str__() + "\t" + prob.__str__() + "\n")

    def output(self):   #Outputs all answers except Q1A
        with open("Q1B.txt", 'w') as oup:
            for x, y in sorted(self.passFreq.items(), key=lambda x: x[1], reverse=True):
                oup.write(
                    x + "\t" + y.__str__() + "\t" + round(float(self.passFreq[x]) / float(self.alphaTotal) * 100, 2).__str__() + "\n")

        with open("Q2A.txt", 'w') as oup:
            oup.write(round(self.effectiveEntropy, 3).__str__())

        with open("Q2B.txt", 'w') as oup:
            oup.write(round(self.maxEntropy, 3).__str__())

        with open("Q3A.txt", 'w') as oup:
            oup.write(round(self.uniqueEffectiveEntropy, 3).__str__())

        with open("Q3B.txt", 'w') as oup:
            oup.write(round(self.uniqueMaxEntropy, 3).__str__())

pwa = pwa()
pwa.main()
