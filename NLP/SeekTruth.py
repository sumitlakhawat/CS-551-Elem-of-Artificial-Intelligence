# SeekTruth.py : Classify text objects into two categories
#
# Shruti Padole, Rajdeep Chauhan, Sumit Lakhawat
# spadole, rajchauh, slakhawa
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import traceback
import re
from numpy import prod


def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    initial_truthful_prob = len([each for each in train_data['labels'] if each =='truthful'])/len(train_data['labels'])
    initial_deceptive_prob = len([each for each in train_data['labels'] if each =='deceptive'])/len(train_data['labels'])
    t_likelihood, d_likelihood = calculate_likelihoods(train_data)
    test_labels = []
    test_sents = cleansents(test_data["objects"])
    try:
        for sent in test_sents:
            sent = sent.split(" ")
            sent = [each for each in sent if each in t_likelihood and each in d_likelihood and each != '']
            truth_prob = [t_likelihood[token] for token in sent]
            decep_prob = [d_likelihood[token] for token in sent]
            if prod(truth_prob)*initial_truthful_prob > prod(decep_prob)*initial_deceptive_prob:
                test_labels.append("truthful")
            else:
                test_labels.append("deceptive")
    except Exception as e:
        print(traceback.format_exc())
    return test_labels
    #return [test_data["classes"][0]] * len(test_data["objects"])

def calculate_likelihoods(data):
    truthful = []
    deceptive = []
    for i in range(len(data['labels'])):
        if data['labels'][i] == 'truthful':
            truthful.append(data['objects'][i])
        else:
            deceptive.append(data['objects'][i])
    truthful = cleansents(truthful)
    deceptive = cleansents(deceptive)
    truthful = sum([each.split(' ') for each in truthful], [])
    deceptive = sum([each.split(' ') for each in deceptive], [])

    truthful_word_freq = {}
    for word in truthful:
        if word in truthful_word_freq:
            truthful_word_freq[word] += 1
        else:
            truthful_word_freq[word] = 1

    #ignoring rarely occurring words
    t_rare = {k:v for k,v in truthful_word_freq.items() if v <= 5}
    truthful_word_freq = {k:v for k,v in truthful_word_freq.items() if k not in t_rare}
    total_truth_count = len(truthful) - sum(t_rare.values())

    #dividing by total count of words in truthful reviews
    truthful_word_prob = {k:v/total_truth_count for k,v in truthful_word_freq.items()}

    deceptive_word_freq = {}
    for word in deceptive:
        if word in deceptive_word_freq:
            deceptive_word_freq[word] += 1
        else:
            deceptive_word_freq[word] = 1

    #ignoring rarely occurring words
    d_rare = {k:v for k,v in deceptive_word_freq.items() if v <= 5}
    deceptive_word_freq = {k:v for k,v in deceptive_word_freq.items() if k not in d_rare}
    total_deceptive_count = len(deceptive) - sum(d_rare.values())

    #dividing by total count of words in deceptive reviews
    deceptive_word_prob = {k:v/total_deceptive_count for k,v in deceptive_word_freq.items()}
    return truthful_word_prob, deceptive_word_prob

def cleansents(sents):
    sents = [each.lower().strip() for each in sents]
    sents = [re.sub(r"([,\.\"'\?\-\*\(\)$_\!~%\\\/\+\;\:\[\]#])", r" ", sent) for sent in sents] #removing punctuations
    #sents = [re.sub(r"([,\.\"'\?\-\*\(\)$_\!~%\\\/\+\;\:\[\]#])(?!\s)", r"\1 ", sent) for sent in sents]
    #sents = [re.sub(r"(?<!\s)([,\.\"'\?\-\*\(\)$_\!~%\\\/\+;\:\[\]#])", r" \1", sent) for sent in sents]
    #sents = [re.sub(r"([a-z]+)([0-9]+)", r"\1 \2", sent) for sent in sents]
    #sents = [re.sub(r"([0-9]+)([a-z]+)", r"\1 \2", sent) for sent in sents]
    sents = [re.sub(r"([0-9])", r" ", sent) for sent in sents] #removing digits
    sents = [re.sub(r"(\bi\b|\bam\b|\bwas\b|\bto\b|\bbe\b|\bat\b|\bthe\b|\bon\b|\bfor\b)", r"", sent) for sent in sents] #removing extra spaces
    sents = [re.sub(r"(\s\s+)", r" ", sent) for sent in sents] #removing extra spaces
    return sents

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
