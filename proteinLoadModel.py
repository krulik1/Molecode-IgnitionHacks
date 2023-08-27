from Bio import SeqIO
import numpy as np
import tensorflow as tf
import keras
from keras.utils import to_categorical
from keras import layers
import random

def predict(file):
    #import fasta sequences !!! replace with path to fasta
    fasta_sequences = SeqIO.parse(open(file),'fasta')

    #mapping string categories to integers
    AAmap = {'A': 1,
        'R': 2,
        'N': 3,
        'D': 4,
        'C': 5,
        'Q': 6,
        'E': 7,
        'G': 8,
        'H': 9,
        'I': 10,
        'L': 11,
        'K': 12,
        'M': 13,
        'F': 14,
        'P': 15,
        'S': 16,
        'T': 17,
        'W': 18,
        'Y': 19,
        'V': 20,
        "0": 0,
        "1": 0}

    #padding sequences and converting into np array
    sequences = []

    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        sequences.append(list(map(AAmap.get, list(sequence.ljust(1670,"0")))))

    sequences = np.array(sequences)

    #performing one hot encoding 
    X = []

    for c,protein in enumerate(sequences):
        
        protein[protein == None] = 0
        X.append(np.asarray(tf.one_hot(protein, 21).numpy()).astype('float32'))

    #casting data into float32
    X = np.asarray(X).astype('float32')

    #load model !!! replace with path to model !!!
    model = keras.models.load_model("projects\Molecode\proteinPredict.keras")

    # Generate predictions
    #print("Generate predictions:")

    predictions = model.predict(X)

    #print("predictions shape:", predictions.shape)
    return predictions

#given a fasta file, predictions are outputted as a numpy array










