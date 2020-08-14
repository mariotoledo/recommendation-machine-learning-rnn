from keras.models import load_model
import pickle
import os
import matplotlib.pyplot as plt
from datetime import datetime
from keras import backend as K

RESULTS_PARENT_DIRECTORY = "results"

def recall_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

model = load_model('cenary1.h5', custom_objects={"recall_m": recall_m, "precision_m": precision_m, "f1_m": f1_m})
history = pickle.load(open("cenary1-history.p", "rb"))

print('Trying to create results directory...')
currentDatetime = datetime.now()
resultsDirectory = "%s/lstm-%s" % (RESULTS_PARENT_DIRECTORY, currentDatetime.strftime("%d-%m-%Y-%H:%M:%S"))

try:
    os.mkdir(resultsDirectory)
except OSError:
    print ("Creation of the directory %s failed" % resultsDirectory)
    exit()
else:
    print ("Successfully created the directory %s " % resultsDirectory)

print(' >>>>>>>>>>>>>> PASSOU DAQUI')

accuracy = plt.figure()
plt.plot(history['recall_m'])
plt.title('model recall_m')
plt.ylabel('recall_m')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
accuracy.savefig("%s/%s" % (resultsDirectory, '/recall_m.png'), dpi=accuracy.dpi)

val_accuracy = plt.figure()
plt.plot(history['val_recall_m'])
plt.title('model accuracy')
plt.ylabel('val_recall_m')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
val_accuracy.savefig("%s/%s" % (resultsDirectory, '/val_recall_m.png'), dpi=val_accuracy.dpi)