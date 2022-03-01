###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids:
# Rajdeep Singh Chauhan rajchauh
# Shruti Padole spadole
# Sumit Lakhawat slakhawa
# (Based on skeleton code by D. Crandall)
#


import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!

    def posterior(self, model, sentence, label):
        if model == "Simple":
            prob = 0
            for i in range(len(sentence)):
                emission = math.log(1/len(self.POS_TAGS))
                if sentence[i] in self.emission_prob:
                    emission = self.emission_prob[sentence[i]][label[i]]
                prob += emission + self.word_prob[label[i]]
            return -prob
        elif model == "HMM":
            prob = 0
            for i in range(len(sentence)):
                if i == 0:
                    emission = math.log(1/len(self.POS_TAGS))
                    if sentence[i] in self.emission_prob:
                        emission = self.emission_prob[sentence[i]][label[i]]
                    prob += emission + self.init_prob[label[i]]
                else:
                    emission = math.log(1/len(self.POS_TAGS))
                    if sentence[i] in self.emission_prob:
                        emission = self.emission_prob[sentence[i]][label[i]]
                    prob += emission + self.transition_prob[label[i-1]][label[i]]
            return -prob
        elif model == "Complex":
            post = self.get_bayes_prob(sentence, label)
            if post == 0:
                return -999
            else:
                return math.log(post)
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        self.POS_TAGS = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.' ]

        init_prob = {pos: 0 for pos in self.POS_TAGS}
        word_prob = {pos: 0 for pos in self.POS_TAGS}
        transition_prob = {pos: {pos2: 0 for pos2 in self.POS_TAGS} for pos in self.POS_TAGS}
        prev_transition_prob = {pos: {pos2: 0 for pos2 in self.POS_TAGS} for pos in self.POS_TAGS}
        emission_prob = {}
        prev_emission_prob = {}
        for (sen, pos_sen) in data:
            for i in range(0, len(sen)):
                word_prob[pos_sen[i]] += 1

                if sen[i] in emission_prob:
                    emission_prob[sen[i]][pos_sen[i]] += 1
                else:
                    emission_prob[sen[i]] = {pos: 0 for pos in self.POS_TAGS}
                    emission_prob[sen[i]][pos_sen[i]] += 1

                if i == 0:
                    init_prob[pos_sen[i]] += 1
                elif i == 1:
                    transition_prob[pos_sen[i-1]][pos_sen[i]] += 1

                    if sen[i] in prev_emission_prob:
                        prev_emission_prob[sen[i]][pos_sen[i-1]] += 1
                    else:
                        prev_emission_prob[sen[i]] = {pos: 0 for pos in self.POS_TAGS}
                        prev_emission_prob[sen[i]][pos_sen[i-1]] += 1
                else:
                    transition_prob[pos_sen[i-1]][pos_sen[i]] += 1
                    prev_transition_prob[pos_sen[i-2]][pos_sen[i]] += 1
                    if sen[i] in prev_emission_prob:
                        prev_emission_prob[sen[i]][pos_sen[i-1]] += 1
                    else:
                        prev_emission_prob[sen[i]] = {pos: 0 for pos in self.POS_TAGS}
                        prev_emission_prob[sen[i]][pos_sen[i-1]] += 1


        init_prob_total = sum(init_prob.values())
        for each in init_prob:
            if init_prob[each] == 0:
                init_prob[each] = -math.log(10 ** -2)
            else:
                init_prob[each] = -math.log(init_prob[each] / init_prob_total)

        word_prob_total = sum(word_prob.values())
        for each in word_prob:
            if word_prob[each] == 0:
                word_prob[each] = -math.log(10 ** -2)
            else:
                word_prob[each] = -math.log(word_prob[each] / word_prob_total)

        for each in transition_prob:
            transition_prob_total = sum(transition_prob[each].values())
            for each2 in transition_prob[each]:
                if transition_prob[each][each2] == 0:
                    transition_prob[each][each2] = -math.log(10 ** -2)
                else:
                    transition_prob[each][each2] = -math.log(transition_prob[each][each2] / transition_prob_total)

        for each in prev_transition_prob:
            prev_transition_prob_total = sum(prev_transition_prob[each].values())
            for each2 in prev_transition_prob[each]:
                if prev_transition_prob[each][each2] == 0:
                    prev_transition_prob[each][each2] = -math.log(10 ** -2)
                else:
                    prev_transition_prob[each][each2] = -math.log(prev_transition_prob[each][each2] / prev_transition_prob_total)

        for each in emission_prob:
            emission_prob_total = sum(emission_prob[each].values())
            for each2 in emission_prob[each]:
                if emission_prob[each][each2] == 0:
                    emission_prob[each][each2] = -math.log(10 ** -2)
                else:
                    emission_prob[each][each2] = -math.log(emission_prob[each][each2] / emission_prob_total)

        for each in prev_emission_prob:
            prev_emission_prob_total = sum(prev_emission_prob[each].values())
            for each2 in prev_emission_prob[each]:
                if prev_emission_prob[each][each2] == 0:
                    prev_emission_prob[each][each2] = -math.log(10 ** -2)
                else:
                    prev_emission_prob[each][each2] = -math.log(prev_emission_prob[each][each2] / prev_emission_prob_total)

        self.init_prob = init_prob
        self.word_prob = word_prob
        self.transition_prob = transition_prob
        self.prev_transition_prob = prev_transition_prob
        self.emission_prob = emission_prob
        self.prev_emission_prob = prev_emission_prob


    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        output = []
        posterior = 0
        for word in sentence:
            probs = {}
            for pos in self.POS_TAGS:
                emission = -math.log(1/len(self.POS_TAGS))
                if word in self.emission_prob:
                    emission = self.emission_prob[word][pos]
                probs[pos] = self.word_prob[pos] + emission
            output.append(min(probs, key=probs.get))
            posterior += probs[min(probs, key=probs.get)]

        self.simplified_posterior = -posterior
        return output

    def hmm_viterbi(self, sentence):
        N=len(sentence)
        V_table = {key: [0] * N for key in self.POS_TAGS}
        which_table = {key: [0] * N for key in self.POS_TAGS}

        for s in self.POS_TAGS:
            emission = -math.log(1/len(self.POS_TAGS))
            if sentence[0] in self.emission_prob:
                emission = self.emission_prob[sentence[0]][s]
            V_table[s][0] = self.init_prob[s] + emission

        for i in range(1, N):
            for s in self.POS_TAGS:
                (which_table[s][i], V_table[s][i]) =  min( [ (s0, V_table[s0][i-1] + 
        self.transition_prob[s0][s]) for s0 in self.POS_TAGS ], key=lambda l:l[1] )

                emission = -math.log(1/len(self.POS_TAGS))
                if sentence[i] in self.emission_prob:
                    emission = self.emission_prob[sentence[i]][s]
                V_table[s][i] += emission

        viterbi_seq = [""] * N
        last_pos = ''
        last_prob = 10000000
        for s in self.POS_TAGS:
            if last_prob > V_table[s][N-1]:
                last_pos = s
                last_prob = V_table[s][N-1]

        self.final_viterbi_posterior = -last_prob
        viterbi_seq[N-1] = last_pos
        for i in range(N-2, -1, -1):
            viterbi_seq[i] = which_table[viterbi_seq[i+1]][i+1]

        return viterbi_seq

    def get_bayes_prob(self, sentence, labels, index = None):
        prob = 1
        for i in range(0, len(sentence)):
            if i == 0:
                word_prob = 1/len(self.POS_TAGS)
                if labels[i] in self.word_prob:
                    word_prob = math.exp(- self.word_prob[labels[i]])

                emission_prob = 1/len(self.POS_TAGS)
                if sentence[i] in self.emission_prob:
                    emission_prob = math.exp(- self.emission_prob[sentence[i]][labels[i]])
                prob = prob * word_prob * emission_prob
            elif i == 1:
                emission_prob = 1/len(self.POS_TAGS)
                if sentence[i] in self.emission_prob:
                    emission_prob = math.exp(- self.emission_prob[sentence[i]][labels[i]])
                transition_prob = 1/len(self.POS_TAGS)
                if labels[i-1] in self.transition_prob:
                    transition_prob = math.exp(- self.transition_prob[labels[i-1]][labels[i]])
                prev_emission_prob = 1/len(self.POS_TAGS)
                if sentence[i] in self.prev_emission_prob:
                    prev_emission_prob = math.exp(- self.prev_emission_prob[sentence[i]][labels[i-1]])
                prob = prob * transition_prob * emission_prob * prev_emission_prob
            else:
                emission_prob = 1/len(self.POS_TAGS)
                if sentence[i] in self.emission_prob:
                    emission_prob = math.exp(- self.emission_prob[sentence[i]][labels[i]])
                transition_prob = 1/len(self.POS_TAGS)
                if labels[i-1] in self.transition_prob:
                    transition_prob = math.exp(- self.transition_prob[labels[i-1]][labels[i]])
                prev_emission_prob = 1/len(self.POS_TAGS)
                if sentence[i] in self.prev_emission_prob:
                    prev_emission_prob = math.exp(- self.prev_emission_prob[sentence[i]][labels[i-1]])
                prev_transition_prob = 1/len(self.POS_TAGS)
                if labels[i-2] in self.prev_transition_prob:
                    prev_transition_prob = math.exp(- self.prev_transition_prob[labels[i-2]][labels[i]])
                prob = prob * transition_prob * emission_prob * prev_emission_prob * prev_transition_prob
        return prob

    def complex_mcmc(self, sentence):

        def get_random(prob_list):
            random_value = random.random()
            for i in range(len(prob_list)):
                if random_value < prob_list[i]:
                    return i
        
        sample = [self.POS_TAGS[get_random([(i+1) * (1/len(self.POS_TAGS)) for i in range(len(self.POS_TAGS))])] for i in range(len(sentence))]

        all_samples = []
        all_samples .append(sample)

        for i in range(0,20):
            new_sample = [* sample]

            for j in range(len(sentence)):
                all_probs = []
                for pos in self.POS_TAGS:
                    new_sample[j] = pos
                    all_probs.append(self.get_bayes_prob(sentence, new_sample, i))

                total_all_prob = sum(all_probs)
                for k in range(0, len(all_probs)):
                    if total_all_prob == 0:
                        all_probs[k] = 1/len(self.POS_TAGS)
                    else:
                        all_probs[k] = all_probs[k] / total_all_prob

                for k in range(1, len(all_probs)):
                    all_probs[k] += all_probs[k-1]
                new_sample[j] = self.POS_TAGS[get_random(all_probs)]
            sample = new_sample
            all_samples.append(new_sample)

        final = []
        for i in range(len(sentence)):
            count_pos = {pos:0 for pos in self.POS_TAGS}
            for sample_1 in all_samples:
                count_pos[sample_1[i]] += 1
            final.append(max(count_pos,key=count_pos.get))
        self.complex_mcmc_posterior = -self.get_bayes_prob(sentence, final)
        return final



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

