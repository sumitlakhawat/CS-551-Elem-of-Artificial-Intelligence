## Optical Character Recognition

### Problem Statement  
- Design a program to extract text from a noisy image using HMM.
- Use the image of defined language as training and learn the representation of each character.
- Use the text document in order to learn English words and flow of the language.
- Current code ingests the image file and returns a list of lists which is just a two-dimensional representation of the characters in the form of black and white dots.
- Define an HMM with apt initial, transition and emission probabilities for training 
- Use this trained classifier to detect meaningful text in the input noisy images by implementing the following two approaches:
    - Based on the diagrams in Part 1, implement simple Bayes Nets for image to text conversion.
    - For the second approach, use richer dependencies and apply Viterbi to the HMM in order to extract text using MAP inference.
- The program will take a noisy image as input and will output the text extracted by both the approaches.

### Design Decisions
- Implemented probabilities:-
- Initial - count_of_each_letter_at_start_of_sentence/number_of_lines
- Transition - count_of_transition_for_one_letter_to_other/all_transitions_from_the_first_letter
- Emission - For emission assigned weights to each possibility:-
    - stars match in both train and test character
    - space match in both train and test character
    - stars in train but not in test
    - space in train but not in test
        - Multiplied all (weight_of_possibility ** count_of_possibility) for each test data
    - Final emission probability for any test character is:- train_letter_weight_for_test_char/sum_of_all_train_letter_for_test_char

- Simple - Used the letter_prob * emission_prob to get trained letter for each test letter in test sentence.
- Viterbi- Used all the above mentioned probabilities to calculate the Viterbi expected path for the test sentence.

### Assumptions Made
- All images contain English words.
- All text in a given image is of same width, font and size.(16x25 pixels)
- Language consists of 26 uppercase and 26 lowercase alphabets, 10 digits and 7 punctuation marks

