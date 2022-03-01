#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (
# Rajdeep Singh Chauhan rajchauh
# Shruti Padole spadole
# Sumit Lakhawat slakhawa
# )
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    # print(im.size)
    # print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def perform_MAP_inference(train_letters, train_text, test_letters):
    (init_prob, transition_prob) = get_all_prob(train_text, train_letters)

    return viterbi(init_prob, transition_prob, test_letters, get_emission(test_letters, train_letters), train_letters)

def get_all_prob(train_text, train_letters):
    
    lines = train_text
    init_prob = {key: 0 for key in train_letters}

    transition_prob = {key1: {key2: 0 for key2 in train_letters} for key1 in train_letters }

    for line in lines:
        if len(line) > 0:
            if line[0] in init_prob:
                init_prob[line[0]] += 1
            for idx in range(1, len(line)):
                if line[idx-1] in init_prob and line[idx] in init_prob:
                    transition_prob[line[idx-1]][line[idx]] += 1
                    if line[idx-1] in 'abcdefghijklmnopqrstuvwxyz':
                        transition_prob[line[idx-1].upper()][line[idx]] += 1
                        if line[idx] in 'abcdefghijklmnopqrstuvwxyz':
                            transition_prob[line[idx-1].upper()][line[idx].upper()] += 1
                    else:
                        if line[idx] in 'abcdefghijklmnopqrstuvwxyz':
                            transition_prob[line[idx-1]][line[idx].upper()] += 1

    total_init_prob_sum = 0
    for each in init_prob:
        init_prob[each] = init_prob[each]/len(lines)
        total_init_prob_sum += init_prob[each]

    for each in init_prob:
        init_prob[each] = init_prob[each]/total_init_prob_sum
        init_prob[each] = -math.log(init_prob[each] if init_prob[each] > 0 else 10 ** -10)
    
    for each in transition_prob:
        total_count = 0
        for each_letter in transition_prob[each]:
            total_count += transition_prob[each][each_letter]
        
        for each_letter in transition_prob[each]:
            transition_prob[each][each_letter] = pow(10,-10) if transition_prob[each][each_letter] == 0 else transition_prob[each][each_letter] / total_count
            transition_prob[each][each_letter] = -math.log(transition_prob[each][each_letter])
    return (init_prob, transition_prob)

def perform_train_text(train_txt_fname):
    lines=[]
    with open(train_txt_fname, "r") as f:
        for line in f:
            lines.append(line)
    return lines

def get_emission(test, train):
    emission = []
    for i in range(0, len(test)):
        emission_prob = {key: 0 for key in train}
        total = 0
        for j in train:
            stars_match = 0
            stars_non_match = 0
            space_match = 0
            space_non_match = 0
            for k in range(0, CHARACTER_HEIGHT):
                for l in range(0, CHARACTER_WIDTH):
                    if train[j][k][l] == '*':
                        if test[i][k][l] == train[j][k][l]:
                            stars_match += 1
                        else:
                            stars_non_match += 1
                    else:
                        if test[i][k][l] == train[j][k][l]:
                            space_match += 1
                        else:
                            space_non_match += 1
            emission_prob[j] = (0.95 ** stars_match) * (0.05 ** space_non_match) * (0.7 ** space_match) * (0.45 ** stars_non_match)
            total += emission_prob[j]
            emission_prob[j] = -math.log(emission_prob[j] if emission_prob[j] > 0 else 10 ** -1000)
        for j in train:
            emission_prob[j] = emission_prob[j] + math.log(total)
        emission.append(emission_prob)
    return emission

import math
def viterbi(initial, transition, observed_states, emission, train_letters):
    N=len(observed_states)
    V_table = {key: [0] * N for key in train_letters}
    which_table = {key: [0] * N for key in train_letters}

    for s in train_letters:
        V_table[s][0] = initial[s] + emission[0][s]

    for i in range(1, N):
        for s in train_letters:
            (which_table[s][i], V_table[s][i]) =  min( [ (s0, V_table[s0][i-1] + 
    transition[s0][s]) for s0 in train_letters ], key=lambda l:l[1] )
            V_table[s][i] += emission[i][s]
    viterbi_seq = [""] * N
    last_char = ''
    last_prob = 10000000
    for s in train_letters:
        if last_prob > V_table[s][N-1]:
            last_char = s
            last_prob = V_table[s][N-1]

    viterbi_seq[N-1] = last_char
    for i in range(N-2, -1, -1):
        viterbi_seq[i] = which_table[viterbi_seq[i+1]][i+1]

    return str(''.join(viterbi_seq))

def simple(emission):
    simple_text = ''
    for i in range(len(emission)):
        simple_text = simple_text + min(emission[i], key=emission[i].get)
    return simple_text


#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
# print("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
# print("\n".join([ r for r in test_letters[0] ]))

train_text = perform_train_text(train_txt_fname)

# The final two lines of your output should look something like this:
print("Simple: " + simple(get_emission(test_letters, train_letters)))
print("   HMM: " + perform_MAP_inference(train_letters, train_text, test_letters))


