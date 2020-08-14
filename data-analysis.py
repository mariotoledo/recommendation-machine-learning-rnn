import operator
import matplotlib.pylab as matplotlib
import os
from datetime import datetime
import json

FILE_INPUT_PATH = "files/user_behavior.txt"
RESULTS_PARENT_DIRECTORY = "results"

numberOfLines = 0
numberOfPages = 0

def countPagesFromLine(pagesLine, pagesCounterDict):
    global numberOfPages
    pages = pagesLine.split()

    for page in pages:
        numberOfPages = numberOfPages + 1
        pagesCounterDict[page] = pagesCounterDict[page] + 1 if page in pagesCounterDict else 1

def countPagesFromDataset(dataset):
    global numberOfLines
    pagesCounterDict = dict()

    for line in dataset:
        numberOfLines = numberOfLines + 1
        countPagesFromLine(line, pagesCounterDict)

    return pagesCounterDict

def countFrequencyOfPages(pagesCounterDict):
    frequencyCounterDict = dict()

    for page in pagesCounterDict:
        frequencyCounterDict[pagesCounterDict[page]] = frequencyCounterDict[pagesCounterDict[page]] + 1 if pagesCounterDict[page] in frequencyCounterDict else 1

    return frequencyCounterDict

def countPagesCountPerUserFromDataset(dataset):
    pagesCounterArray = []

    for line in dataset:
        pages = line.split()
        pagesCounterArray.append(len(pages))
    
    return pagesCounterArray

def countAccessFrequencyPerUser(pagesCounterArray):
    frequencyCounterDict = dict()

    for pageCount in pagesCounterArray:
        frequencyCounterDict[pageCount] = frequencyCounterDict[pageCount] + 1 if pageCount in frequencyCounterDict else 1

    return frequencyCounterDict

print('Trying to read %s' % FILE_INPUT_PATH)
dataset = open(FILE_INPUT_PATH,"r")

print('Starting to count number of words...')
pagesCounter = countPagesFromDataset(dataset)

print('Starting to count number of words per user...')
dataset.seek(0)
pagesCountPerUserCounter = countPagesCountPerUserFromDataset(dataset)

print('Calculating most visited pages...')
mostVisitedPage = max(pagesCounter.iteritems(), key=operator.itemgetter(1))[0]

print('Calculating min visited pages...')
leastVisitedPage = min(pagesCounter.iteritems(), key=operator.itemgetter(1))[0]

print('Calculating most visits a user made...')
mostsVisitsByUser = max(pagesCountPerUserCounter)

print('Calculating least visits a user made...')
leastVisitsByUser = min(pagesCountPerUserCounter)

print('Calculating frequency of pages count...')
pageAccessFrequencyCounter = countFrequencyOfPages(pagesCounter)
pageAccessFrequencyCounter = sorted(pageAccessFrequencyCounter.items())

print('Calculating frequency of pages access per user count...')
pageAccessFrequencyPerUserCounter = countAccessFrequencyPerUser(pagesCountPerUserCounter)
pageAccessFrequencyPerUserCounter = sorted(pageAccessFrequencyPerUserCounter.items())

if not os.path.exists(RESULTS_PARENT_DIRECTORY):
    os.makedirs(RESULTS_PARENT_DIRECTORY)

print('Trying to create results directory...')
currentDatetime = datetime.now()
resultsDirectory = "%s/analysis-%s" % (RESULTS_PARENT_DIRECTORY, currentDatetime.strftime("%d-%m-%Y-%H:%M:%S"))

try:
    os.mkdir(resultsDirectory)
except OSError:
    print ("Creation of the directory %s failed" % resultsDirectory)
    exit()
else:
    print ("Successfully created the directory %s " % resultsDirectory)

print('Trying to create summary file...')
resultsFile = open("%s/%s" % (resultsDirectory, "summary.txt") ,"w+")

resultsFile.write('Number of users is %i\n' % numberOfLines)
resultsFile.write('Number of pages is %i\n' % len(pagesCounter))
resultsFile.write('Number of visits on pages is %i\n' % numberOfPages)
resultsFile.write('Average visited pages per user: %i\n' % (numberOfPages / numberOfLines))
resultsFile.write('The most visited page is %s (%i)\n' % (mostVisitedPage, pagesCounter[mostVisitedPage]))
resultsFile.write('The least visited page is %s (%i)\n' % (leastVisitedPage, pagesCounter[leastVisitedPage]))
resultsFile.write('The most visits a user made is %i\n' % mostsVisitsByUser)
resultsFile.write('The least visits a user made is %i\n' % leastVisitsByUser)
resultsFile.close()

print('Trying to create page access frequency log...')
pageAccessFrequencyFile = open("%s/%s" % (resultsDirectory, "page_access_frequency.txt") ,"w+")
pageAccessFrequencyFile.write(json.dumps(pageAccessFrequencyCounter))
pageAccessFrequencyFile.close()

print('Gererating frequency of pages count graph...')
x, y = zip(*pageAccessFrequencyCounter)
pageAccessFrequencyImage = matplotlib.figure()
matplotlib.plot(x, y)
pageAccessFrequencyImage.savefig("%s/%s" % (resultsDirectory, '/pageAccessFrequencyImage.png'), dpi=pageAccessFrequencyImage.dpi)

print('Trying to create page access frequency by user log...')
pageAccessFrequencyFileByUser = open("%s/%s" % (resultsDirectory, "page_access_frequency_by_user.txt") ,"w+")
pageAccessFrequencyFileByUser.write(json.dumps(pageAccessFrequencyPerUserCounter))
pageAccessFrequencyFileByUser.close()

print('Gererating frequency of pages count by user graph...')
x, y = zip(*pageAccessFrequencyPerUserCounter)
pageAccessFrequencyPerUserImage = matplotlib.figure()
matplotlib.plot(x, y)
pageAccessFrequencyPerUserImage.savefig("%s/%s" % (resultsDirectory, '/pageAccessFrequencyImagePerUser.png'), dpi=pageAccessFrequencyPerUserImage.dpi)

dataset.close()