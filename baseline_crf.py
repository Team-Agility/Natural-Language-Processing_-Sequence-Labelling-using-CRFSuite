import pycrfsuite,sys, timeit

start = timeit.default_timer()
#!/usr/bin/env python3

"""hw3_corpus_tools.py: CSCI544 Homework 3 Corpus Code

USC Computer Science 544: Applied Natural Language Processing

Provides three functions and two data containers:
get_utterances_from_file - loads utterances from an open csv file
get_utterances_from_filename - loads utterances from a filename
get_data - loads all the CSVs in a directory
DialogUtterance - A namedtuple with various utterance attributes
PosTag - A namedtuple breaking down a token/pos pair

This code is provided for your convenience. You are not required to use it.
Feel free to import, edit, copy, and/or rename to use in your assignment.
Do not distribute."""

__author__ = "Christopher Wienberg"
__email__ = "cwienber@usc.edu"

from collections import namedtuple
import csv
import glob
import os

def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    #print (dialog_filenames)
    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with 
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)



def sent2labels(sent):

    return [label[0] for label in sent]


def sent2features(sent):
    #print (sent)


    return [word2features(sent," ", i) if i==0 else word2features(sent,sent[i-1][1], i)  for i in range(len(sent))]




def sent2tokens(sent):
    return [token for token in sent]




def word2features(sent, previous, i ):


    features={}
    all_tokens_in_sent=[]
    all_pos_in_sent=[]
    change_speaker=0        #initially there is no change of speaker
    first_utterance=0       #initially, the first sentence is the first utterance

    #current_speaker=sent[i][1]


    if(previous!=sent[i][1]):

        change_speaker=1


    if(i==0): #if previous speaker is blank or single space means that this is the first utterance
        first_utterance=1
        change_speaker = 0

    if(sent[i][2] is not None):
        #all_tokens=sent[i][2]
        len_all_tokens = len(sent[i][2])

        for k in range(0,len_all_tokens):
            #PosTag = sent[i][2][k]

            all_pos_in_sent.append(sent[i][2][k][0]) #appending all POS to the list
            all_tokens_in_sent.append(sent[i][2][k][1])  # appending all tokens to the list








    #assigining features
    features['speaker_change'] = change_speaker
    features['first_utter'] = first_utterance
    features['tokens'] = all_tokens_in_sent
    features['pos'] = all_pos_in_sent





    #print features
    return features




#Code for testing of the functions
y_train =[]
X_train =[]



#path_train=sys.argv[2]

#path_test=sys.argv[1]
path_train = 'C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment3\\data\\predict'    # use this path for the test data

path_test ='C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment3\\data\\test_few_files'  #this is just a temp path only



#t=get_data(path_test)


#print(list(t))
#list_all_dialogue_folder= list(get_data(path_test))       #list_all_dialogue_folder This has all the dialogues




X_train=[sent2features(s) for s in list(get_data(path_test))]
y_train=[sent2labels(s) for s in list(get_data(path_test))]



trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(X_train, y_train):
    trainer.append(xseq, yseq)





trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 250,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

trainer.train('conll2002-esp1.crfsuite')

#Make predictions

tagger = pycrfsuite.Tagger()
tagger.open('conll2002-esp1.crfsuite')




#op=open(sys.argv[3], "a+")
op=open("output.txt","a+")


for root, dirs, files in os.walk(path_train):
    for file in files:
        fpath = os.path.join(root, file)  # fpath contains the fully qualified path
        op.write("Filename=" +"\""       +file   +"\""  +         "\n")
        for pred_tag in tagger.tag(sent2features(get_utterances_from_filename(fpath))):
           op.write(pred_tag+"\n")
        op.write("\n")


stop = timeit.default_timer()

print ("Baseline Total Time:"+str(stop - start))
