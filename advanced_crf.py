import pycrfsuite, sys, timeit

start = timeit.default_timer()
# !/usr/bin/env python3

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
    # print (dialog_filenames)
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

    return [word2features(sent, " ", i) if i == 0 else word2features(sent, sent[i - 1][1], i) for i in range(len(sent))]


def sent2tokens(sent):
    return [token for token in sent]


def word2features(sent, previous, i):
    # print(str(sent)+" "+ "previous:"+str(previous)+ " i:"+ str(i))
    questions = ["who", "what", "when", "where", "why", "which", "would","whose","how"]
    ack = ["uh-huh", "uh", "huh","ok", "okay", "wow", "oh", "sure","um","yep","right","yes","ooh","yeah","really"]
    features = {}

    advance_feat_token = []  # This is the list for the advanced features for token
    advance_feat_pos = []  # This is the list for the advanced pos for each word
    change_speaker = 0  # initially there is no change of speaker
    first_utterance = 0  # initially, the first sentence is the first utterance
    acknowledge = 0  # Uh-huh this is the acknowledgement
    wh_question=0
    uppercase=0
    laughter=0

    # current_speaker=sent[i][1]
    all_tokens_in_sent=[]
    all_pos_in_sent=[]

    if (previous != sent[i][1]):
        change_speaker = 1

    if (i == 0):  # if previous speaker is blank or single space means that this is the first utterance
        first_utterance = 1
        change_speaker = 0

    if(sent[i][2] is None):
        #print("Its none" +str(sent[i]))
        laughter=1

    if (sent[i][2] is not None):
        # all_tokens=sent[i][2]
        len_all_tokens = len(sent[i][2])


        if (len_all_tokens == 2 and (sent[i][2][1][0] == "," or sent[i][2][1][0] == ".")):
            # print(str(sent[i][2][0][0])+str(sent[i][2][1][0]) )

            if (sent[i][2][0][0].lower() in ack):
                #print("len is 2"+sent[i][2][0][0])
                acknowledge = 1

        # print(sent[i][2])



        for k in range(0, len_all_tokens):
            # PosTag = sent[i][2][k]
            # print sent[i][2][k]
            # pos=sent[i][2][k][0]
            # token = sent[i][2][k][1]
            # print(sent[i][2][k][0])
            all_pos_in_sent.append(sent[i][2][k][0]) #appending all POS to the list
            all_tokens_in_sent.append(sent[i][2][k][1])  # appending all tokens to the list

            if (k == 0):
                if (k + 1 == len_all_tokens):  # case ehrn a sentence contains only 1 element then k+1 or next token will throw index out of bound error
                    # print " There is only one element in a sentence"
                    # curr_PosTag = sent[i][2][k]

                    # cur_pos = sent[i][2][k][0]
                    # cur_token = sent[i][2][k][1]

                    if(sent[i][2][k][0].isupper()):
                        #print("Yes it has upper cased string in line 150 "+str(sent[i]))
                        uppercase=1

                    if (sent[i][2][k][0].lower() in ack):
                        # print(sent[i][2][k][0])
                        acknowledge = 1



                    advance_feat_token.append(sent[i][2][k][1])
                    advance_feat_pos.append(sent[i][2][k][0])

                else:
                    # curr_PosTag = sent[i][2][k]
                    # next_PosTag = sent[i][2][k + 1]
                    # print ("Number of words in sentence"+str(len(sent[i][2]))+     " Current POS: "+str(curr_PosTag) +"Next POS: "   +str(next_PosTag))
                    # prev_token="_BOS_"        #The previous token is Beginning of a sentence hence no prev token
                    # prev_pos="_BOS_"

                    # cur_pos = curr_PosTag[0]
                    # cur_token = curr_PosTag[1]

                    # next_token = next_PosTag[1]
                    # next_pos = next_PosTag[0]
                    # print(str(sent[i][2][k][0]))

                    if(sent[i][2][k][0][0].isupper()):
                        #print("Yes it has upper case in line 175"+str(sent[i]))
                        uppercase=1

                    if (sent[i][2][k][0].lower() in questions):
                        #print("Questions "+str(sent[i][2][k][0]) )
                        wh_question=1

                        #print("End of sentence in line 189"+ str(sent[i][2][k][0]))

                    advance_feat_token.append(sent[i][2][k][1])
                    advance_feat_pos.append(sent[i][2][k][0])


            elif (k <=(len_all_tokens - 1)):
                # prev_PosTag=sent[i][2][k-1]
                # curr_PosTag=sent[i][2][k]
                # next_PosTag=sent[i][2][k+1]

                # prev_token=prev_PosTag[1]
                # cur_token=curr_PosTag[1]
                # next_token=next_PosTag[1]

                # prev_pos=prev_PosTag[0]
                # cur_pos=curr_PosTag[0]
                # next_pos=next_PosTag[0]

                # advance_feat_token.append(prev_token)
                # advance_feat_token.append(cur_token)
                # advance_feat_token.append(next_token)

                # advance_feat_pos.append(prev_pos)
                # advance_feat_pos.append(cur_pos)
                # advance_feat_pos.append(next_pos)


                if (sent[i][2][k - 1][0] in questions or sent[i][2][k][0] in questions):
                    wh_question=1



                advance_feat_token.append(sent[i][2][k-1][1]+" "+sent[i][2][k][1])
                advance_feat_pos.append(sent[i][2][k-1][0]+" "+sent[i][2][k][0])


    # assigining features
    features['speaker_change'] = change_speaker
    features['first_utter'] = first_utterance
    features['adv_feat_tokens'] = advance_feat_token
    features['adv_feat_pos'] = advance_feat_pos
    features['acknowledgement'] = acknowledge
    features['tokens'] = all_tokens_in_sent
    features['pos'] = all_pos_in_sent
    features['wh_question'] =wh_question
    features['uppercase'] =uppercase
    features['laughter']=laughter

    #print features
    return features


# Code for testing of the functions
y_train = []
X_train = []

# path_train=sys.argv[2]

# path_test=sys.argv[1]

path_train = 'C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment3\\data\\predict'  # use this path for the test data

path_test = 'C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment3\\data\\test_few_files'  # this is just a temp path only

t = get_data(path_test)

# print(list(t))
list_all_dialogue_folder = list(t)  # list_all_dialogue_folder This has all the dialogues

X_train = [sent2features(s) for s in list_all_dialogue_folder]
y_train = [sent2labels(s) for s in list_all_dialogue_folder]

# print (str(X_train))
##################################################################This is the training the model and tagging the test data##########################################



trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(X_train, y_train):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,  # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 100,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

trainer.train('conll2002-esp2.crfsuite')

# Make predictions

tagger = pycrfsuite.Tagger()
tagger.open('conll2002-esp2.crfsuite')

op = open("output.txt", "a+")

# op=open(sys.argv[3], "a+")



for root, dirs, files in os.walk(path_train):
    for file in files:
        fpath = os.path.join(root, file)  # fpath contains the fully qualified path
        op.write("Filename=" + "\"" + file + "\"" + "\n")
        for pred_tag in tagger.tag(sent2features(get_utterances_from_filename(fpath))):
            op.write(pred_tag + "\n")
        op.write("\n")

stop = timeit.default_timer()

print ("Advanced Total Time:" + str(stop - start))

