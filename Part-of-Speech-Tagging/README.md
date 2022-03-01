## Part-of-speech Tagging

### Problem Statement  
- Design a program to label sentences with correct POS-tags.
- A large corpus of labelled training as well as testing data is provided consisting of tokenized sentences and corresponding POS-tag for each token.
- Based on the dependencies shown in the diagram, implement Bayes Nets in three ways to generate Part-Of-Speech tags for input sentences:
    - Use Simple Bayes Nets to estimate most probable POS tags for input sentence.
    - Use a richer Bayes Net with inter-word dependencies and then apply Viterbi to find the maximum a posteriori labeling for the input sentence.
    - Finally, use even richer dependencies between successive words and POS tags and generate thousands of samples i.e. use Gibb's Sampling method and then return whichever POS tag occurred most for each word in the input sentence.
- For each input sentence, the program should use the training corpus and generate a list of labels using all three approaches listed above and also output the log(joint probability) for each approach.


### Design Decisions
- As part of **training data**, we created dictionaries to maintain various dependencies illustrated in the diagram.
- **Initial_probablity** maintains the probability of each pos tag occurring at the start of a sentence
- **Word_Probability** maintains the probability of any POS tag occurring in the entire training data
- **Transisiton_Probability** stores the probabilities of any two POS tags occurring in succession, For ,eg:- "The" -> "ocean"
- **Emission_Probability** stores the probabilities of any word belonging to a certain POS tag in the training data
- **Previous_Transition_Probability** holds the probabilities of any POS Tag occurring after the POS tag following the current POS tag.
    EG: For, a sentence with labels, *Pos1>Pos2>Pos3*, the Previous_Transition_Probability dict calculates `P(Pos1, Pos3)`
- **Previous_Emission_Probability** holds the probabilities of any word belonging to a POS tag and the same word being preceded by a word belonging to a certain POS tag.
    EG: For, a sentence *W1>W2>W3* with labels, *Pos1>Pos2>Pos3*, the Previous_Emission_Probability dict calculates `P(W2,Pos2,Pos1)`
- Computed all the probabilities as **-math.log(_prob_)**
- As part of the **Simplified Bayes Nets** approach, we simply calculated the sum of logs of Word_Probabilities and Emission_Probabilities and assigned the POS tag with the minimum value to the token.
- For the **HMM_Viterbi** approach, Followed these steps:-
    - Computed different probabilities:- Initial, Transition and Emission.
    - Used the Bayes NET used for HMM.
    - Now started computing the Viterbi table, starting with initialising first column probabilities(containing all possible POS for first word) as Initial_probability.
    - For the next iteration **t**, for each POS tag computed V[t-1][pos] + Transition[pos(t-1)][pos(t)] for next word. Get the minimum of this value and assign previous pos in which table and assign V[t] as V[t-1][pos] + Transition[pos(t-1)][pos(t)] + Emission[word][pos(t)].
    - Keep iterating the process till the last word of test sentence.
    - Get the min POS of all the POS prob values for last word and start back track from last POS using which table.
    - This will give us expected sequence of POS for given sentence.

- For the **Complex_MCMC** approach,
    - Used all the above defined probabilities.
    - Used Gibbs Sampling Approach
    - Assigned random POS to each word using equal probability for all POS.
    - Started the iteration of sampling
    - For Each Iteration,
        - Starting from the first word, keeping all other words POS fixed computed bayes net probability for all pos possible for first word.
        - Using random method operating on computed probability selected pos and assigned to first word.
        - Now do the same for next word.
        - Keep iterating till the last word in sentence
        - append data in sample array
     - Keep performing the iteration for a predefined iterations.
     - At the end for each word compute max probability of any POS and declare it as a POS of that word.

- Posteriors are calculated as follows:-
    - Simple - Emission * word_prob for each word and sum them.
    - HMM - Last word probability entry in the Viterbi table
    - Complex - calculated probability according to the bayes net formed in complex MCMC.

- RESULT DATA ON 2000 sentence test data:-

                  Simple     HMM Complex it's  late  and   you   said  they'd be    here  by    dawn  ''    .    
0. Ground truth   -33.25  -27.77  -76.16 prt   adv   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
      1. Simple   -31.62  -26.17  -73.73 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
         2. HMM   -31.62  -26.17  -73.73 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
     3. Complex   -37.18  -28.99  -70.04 det   adj   noun  pron  verb  prt    verb  adv   adp   noun  .     .    

So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       92.72%               42.05%
            2. HMM:       93.70%               47.25%
        3. Complex:       83.28%               16.30%

----
