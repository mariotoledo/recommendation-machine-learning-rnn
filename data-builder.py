import random
import os
from datetime import datetime

CONFIG_FILE_PATH = "files/config.json" 
FILE_INPUT_PATH = "files/user_behavior.txt"
RESULTS_DIRECTORY = "processed_data"
DATA_PROPORTION = 0.005

print('Trying to read %s' % FILE_INPUT_PATH)
dataset = open(FILE_INPUT_PATH,"r")
data = list()
for line in dataset:
    data.append(line)
dataset.close()

if not os.path.exists(RESULTS_DIRECTORY):
    os.makedirs(RESULTS_DIRECTORY)
    print('created directory %s' % RESULTS_DIRECTORY)

train_data = data[:int((len(data) + 1) * DATA_PROPORTION)]

print('Trying to create train data file with %s%% of database' % DATA_PROPORTION)
trainDataFile = open("%s/%s.txt" % (RESULTS_DIRECTORY, DATA_PROPORTION) ,"w+")

for line in train_data:
    trainDataFile.write(line)
trainDataFile.close()    

print('Finished')