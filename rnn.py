import numpy as np
np.random.seed(42)
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GRU, LSTM
from keras.layers import Dropout
from keras.layers.core import Dense, Activation, Dropout, RepeatVector
from keras.utils import np_utils
from keras.optimizers import RMSprop
from keras.optimizers import SGD
from keras.optimizers import Adagrad
from keras.optimizers import Adam
import metrics
import pickle
import json
import os
import itertools as it
from pandas import DataFrame
from keras.utils import plot_model


#CONFIG_FILE_PATH = "files/config-test.json"
CONFIG_FILE_PATH = "files/config.json"
RESULTS_DIRECTORY = "results"

DATASET_PATH = "processed_data/0.001.txt"
MAX_SEQUENCE_LENGTH = 40
NUMBER_OF_UNITS = 128
RNN_TYPE = 'lstm-gru'

def buildExperimentsCombination(configJson):
    experiments = list()

    allValues = list(configJson)
    combinations = it.product(*(config[configKey] for configKey in allValues))
    experimentNumber = 1
    combinationList = list(combinations)

    for combination in combinationList:
        experiment = dict()
        experiment['experimentId'] = 'experiment-%i' % experimentNumber
        attributeIndex = 0

        for attribute in configJson:
            experiment[attribute] = combination[attributeIndex]
            attributeIndex += 1

        experimentNumber += 1
        experiments.append(experiment)

    return experiments

def getOptimizerFromName(optimizer):
    if optimizer == 'SGD':
        return SGD(learning_rate=0.01, momentum=0.0, nesterov=False)
    elif optimizer == 'Adagrad':
        return Adagrad(learning_rate=0.01)
    elif optimizer == 'Adam':
        return Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
    else:
        return RMSprop(lr=0.01)

def createRNN(type, experimentId, X, y, chars, maxSequenceLength, numberOfUnits, activationFunction, epochs, optimizerName, batchSize, dataFrameDict):
    model = Sequential()
    if(type == 'lstm'):
        model.add(LSTM(numberOfUnits, input_shape=(maxSequenceLength, len(chars))))
    elif(type == 'gru'):
        model.add(GRU(numberOfUnits, input_shape=(maxSequenceLength, len(chars))))
    elif(type == 'lstm-gru'):
        model.add(GRU(numberOfUnits, input_shape=(maxSequenceLength, len(chars)), return_sequences=True))
        model.add(LSTM(numberOfUnits, input_shape=(maxSequenceLength, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation(activationFunction))

    optimizer = getOptimizerFromName(optimizerName)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy', metrics.recall, metrics.precision, metrics.f1_score])
    model.summary()

    plot_model(model, show_shapes=True, show_layer_names=True, to_file='model-lstm-gru.png')
    from IPython.display import Image
    Image(retina=True, filename='model.png')

    history = model.fit(X, y, validation_split=0.2, batch_size=batchSize, epochs=epochs, shuffle=True).history

    resultsDirectory = '%s/lstm-gru' % RESULTS_DIRECTORY

    if not os.path.exists(resultsDirectory):
        os.makedirs(resultsDirectory)
        print('created directory %s' % resultsDirectory)

    resultsFile = open("%s/%s.txt" % (resultsDirectory, experimentId) ,"w+")
    resultsFile.write('accuracy %f\n' % history['accuracy'][epochs - 1])
    resultsFile.write('recall %f\n' % history['recall'][epochs - 1])
    resultsFile.write('precision %f\n' % history['precision'][epochs - 1])
    resultsFile.write('f1_score %f\n' % history['f1_score'][epochs - 1])
    resultsFile.close()

    dataFrameDict['experimentId'].append(experimentId)
    dataFrameDict['type'].append('lstm')
    dataFrameDict['accuracy'].append(history['accuracy'][epochs - 1])
    dataFrameDict['recall'].append(history['recall'][epochs - 1])
    dataFrameDict['precision'].append(history['precision'][epochs - 1])
    dataFrameDict['fonescore'].append(history['f1_score'][epochs - 1])

    model.summary()

    model.save('%s/%s.h5' % (resultsDirectory, experimentId))
    pickle.dump(history, open("%s/%s.p" % (resultsDirectory, experimentId), "wb"))
    

config = json.load(open(CONFIG_FILE_PATH, "r"))

if not os.path.exists(RESULTS_DIRECTORY):
    os.makedirs(RESULTS_DIRECTORY)
    print('created directory %s' % RESULTS_DIRECTORY)

experiments = buildExperimentsCombination(config)

file = open("%s" % DATASET_PATH ,"r")
dataset = file.read()
file.close()

words = dataset.split()

chars = sorted(list(set(words)))
char_indices = dict((c, i) for i, c in enumerate(chars))

print('unique chars: ', {len(chars)})

sentences = []
next_chars = []
for i in range(0, len(words) - MAX_SEQUENCE_LENGTH, 1):
    sentences.append(words[i: i + MAX_SEQUENCE_LENGTH])
    next_chars.append(words[i + MAX_SEQUENCE_LENGTH])

n_patterns = len(sentences)
n_vocab = len(chars)

print('n_patterns:', n_patterns)
print('n_vocab:', n_vocab)

#HOT ENCODING
X = np.zeros((n_patterns, MAX_SEQUENCE_LENGTH, n_vocab), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
   for t, char in enumerate(sentence):
       X[i, t, char_indices[char]] = 1
   y[i, char_indices[next_chars[i]]] = 1


dataFrameDict = {
    'experimentId': [],
    'type': [],
    'accuracy': [],
    'recall': [],
    'precision': [],
    'fonescore': []
}

for experiment in experiments:
    print("starting %s" % experiment['experimentId'])
    print(experiment)
    createRNN(
        RNN_TYPE,
        experiment['experimentId'], 
        X, 
        y, 
        chars, 
        MAX_SEQUENCE_LENGTH, 
        NUMBER_OF_UNITS, 
        experiment['activation_function'], 
        experiment['epochs'], 
        experiment['optimizer'], 
        experiment['batch_size'],
        dataFrameDict
    )

    print('==========================')

dataFrame = DataFrame(dataFrameDict, columns= ['experimentId', 'type', 'accuracy', 'recall', 'precision',  'fonescore'])
dataFrame.to_csv('%s/results-lstm-gru.csv' % RESULTS_DIRECTORY, index = None, header=True)