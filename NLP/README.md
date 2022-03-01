## Text Classification

### Problem Statement  

- Use Naive Bayes Classifier to classify reviews as *Truthful* or *Deceptive*.
- Input :
   1. Train data dictionary containing\
            - "Objects" : user generated reviews\
            - "Labels"  : ground truth lables corresponding to each review\
            - "Classes" : uniques set of labels, which is always two : truthful & deceptive
   2. Test data dictionary containing\
            - "Objects" : reviews that are to be classified\
            - "Labels"  : ground truth lables corresponding to each review to be used only for accuracy calculation\
            - "Classes" : uniques set of labels, which is always two : truthful & deceptive
- Output : A list of labels that correspond to reviews given in the test data

### Logic Used :

- First, we make two lists of reviews from the training data - Truthful and Deceptive
- We then calculate initial probabilities of any review being truthful or decepetive as shown below:\
   ` p(truthful) = no. or truthful reviews/ total no. of reviews `\
   ` p(deceptive) = no. or deceptive reviews/ total no. of reviews `
- Then we applied basic cleaning rules on each sentence, i.e., converting to lowercase and stripping away extra spaces if any
- We also removed punctuations and a few highly frequent stop words which we believed were causing misclassification to some extent
- We then made a word frequency dictionary for both Truthful and Deceptive reviews.
- We ignored tokens that occurred less than or equal to 5 times in the reviews.
- We then calcualted likelihoods of all tokens by dividing number of occurrences of the token by the total number if words in the reviews in the training data. For eg:\
    ` p(word|truthful) = freq of word in truthful reviews/ total words in all reviews `\
    ` p(word|deceptive) = freq of word in deceptive reviews/ total words in all reviews `
- Then, for each sentence in the test data, we calculate the ratio of the product of probabilities of each word as shown below:\
    ` p(T|w1,w2,w3) / p(D|w1,w2,w3) =  (p(T) * p(w1|T) * p(w2|T) * p(w3|T)) / (p(D) * p(w1|D) * p(w2|D) * p(w3|D)) `
- If the ratio is greater than 1, then the sentence is classified as *Truthful*, else as *Deceptive*

### Problems Faced

- Originally, we used regex to separate all special characters and numbers as separate tokens, but that resulted in a low accuracy. Eventually, we just settled with lowercasing the reviews and stripping away extra spaces. We removed all punctuations in order to consider only alphabetical tokens.
- There were several tokens in the test data that were not present in the training data. There were also tokens in the test data that were either only present in the truthful reviews part of the training data or only in the deceptive part of thee training data. Considering the probability of a token only for the label in which the token was present and not for the other label would cause the classification to skew in favor of the former label. Hence, for such cases, we skipped counting the token for both labels.
