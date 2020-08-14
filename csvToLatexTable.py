def formatStringNumber(stringNumber):
	return stringNumber.replace('.', ',')[:10]

files = [
	"results/lstm.csv",
	"results/gru.csv",
	"results/lstm-gru.csv"
]

for file in files:
	textFile = open("%s.txt" % file,"w+")
	isHeader = True
	with open(file) as csvFile:
		for line in csvFile:
			if(isHeader == False):
				splitedLine = line.split(',')
				newFileLine = '%s & %s & %s & %s & %s' % (splitedLine[0], formatStringNumber(splitedLine[2]), formatStringNumber(splitedLine[3]), formatStringNumber(splitedLine[4]), formatStringNumber(splitedLine[5]))
				if("\n" in newFileLine):
					newFileLine = newFileLine.replace("\n", "")
				newFileLine = '%s \\\\\n' % newFileLine
				textFile.write(newFileLine)
			else:
				isHeader = False
	textFile.close()

for file in files:
	textFile = open("%s-new.csv" % file,"w+")
	with open(file) as csvFile:
		for line in csvFile:
			splitedLine = line.split(',')
			newFileLine = '%s;%s;%s;%s;%s' % (splitedLine[0], formatStringNumber(splitedLine[2]), formatStringNumber(splitedLine[3]), formatStringNumber(splitedLine[4]), formatStringNumber(splitedLine[5]))
			if("\n" in newFileLine):
				newFileLine = newFileLine.replace("\n", "")
			newFileLine = '%s\n' % newFileLine
			textFile.write(newFileLine)
	textFile.close()
