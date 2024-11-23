# Part of Speech Tagging Using Viterbi HMM

This project implements a Hidden Markov Model (HMM) for Part-of-Speech (POS) tagging using the Viterbi algorithm. It utilizes a training corpus to generate prior probabilities (transition and emission probabilities) and applies these probabilities to predict POS tags for a test corpus.

## POS_Training.py:
- Generates a likelihood table for word-to-POS probabilities
- Computes transition probabilities for POS-to-POS transitions
- Handles sentence boundaries using "Begin_S" and "End_S" states
## POS_Tagging.py:
- Implements the Viterbi algorithm for sequence prediction
- Handles Out-of-Vocabulary (OOV) words by assigning a constant likelihood (0.0000001)
- Uses transition and emission probabilities for predictions

## Steps to Run:
1. Use POS_Training.py to train the model. This program reads the training data and creates 2 hash tables for likelihood and transitions. Then, this program writes the contents of the hash table into a txt output file.
    Command:
       `python POS_Training.py <training_corpus> <output_likelihood_transition_file>`
3. Tag the test corpus: Use the POS_Tagging.py script to predict POS tags for a .words file using the generated probabilities.
    Command:
        `python POS_Tagging.py <likelihood_transition_file> <test_corpus>`
    Output: 
        - "output.pos" which is a POS-tagged file
4. Evaluate the Output: Use the score.py script to evaluate the tagged output against a key file.
    Command: 
        `python score.py <corpus_key> <output_file>`
    Output:
        - accuracy score
