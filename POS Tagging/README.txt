Part of Speech Tagging Program

This POS tagging program uses the Viterbi HMM method using the prior probabilities and liklihood tables. All OOV were set to a probability of 0.0000001

How to Run the System:

1. Use POS_Training.py to train the model. This program reads the training data and creates 2 hash tables for likelihood and transitions. Then, this program writes the contents of the hash table into a txt output file.

    Command:
    python POS_Training.py <training_data_file> <output_file_name>

2. Then use POS_Tagging.py to annotate a .words file and output a .pos file. 

    Command:
    POS_Tagging.py <training_data_file> <input_text_file.words>