Noun Group Tagger Using Maximum Entropy

This project implements a Noun Group tagger using a Maximum Entropy (MaxEnt) model. The program processes input files to generate features, trains a MaxEnt model, and uses the model to predict BIO tags for identifying noun groups in a test corpus.

Features Implemented:
    Basic Features
        word: The current word
        POS: Part-of-speech tag of the current word
        CAPITALIZED: Whether the word starts with an uppercase letter
        WORD_SHAPE: The shape of the word (e.g., UPPER, LOWER, CAPITALIZED, MIXED)
        HAS_DIGIT: Whether the word contains a digit
        HAS_HYPHEN: Whether the word contains a hyphen
        LENGTH: Length of the word
        PREFIX_1 and PREFIX_2: First one or two characters of the word
        SUFFIX_1 and SUFFIX_2: Last one or two characters of the word
    Contextual Features
        PREV_WORD and PREV_POS: Word and POS of the previous token
        NEXT_WORD and NEXT_POS: Word and POS of the next token
        PREV2_WORD and PREV2_POS: Word and POS two tokens before
        NEXT2_WORD and NEXT2_POS: Word and POS two tokens after
    Combined Features
        prevpos+pos: Combination of the previous token's POS and the current token's POS
        pos+nextpos: Combination of the current token's POS and the next token's POS
    Advanced Features
        tags-since-dt: Captures all POS tags encountered since the last determiner (DT) or the start of the sentence, sorted alphabetically

Files:
    Input Data
        - WSJ_02-21.pos-chunk: Training file with tokens, POS tags, and BIO tags
        - WSJ_24.pos: Development file for testing feature generation
        - WSJ_24.pos-chunk: Answer key for evaluating the system on the development file
        - WSJ_23.pos: Test file for generating the final output
    Program Files
        - extract_features.py: Python script to generate feature files from input corpora
        - MEtrain.java: Java program to train the MaxEnt model
        - MEtag.java: Java program to use the trained MaxEnt model for tagging
        - score.chunk.py: Python script to evaluate system output against an answer key
    Other Files
        - maxent-3.0.0.jar: Library for MaxEnt modeling
        - trove.jar: Library dependency for MaxEnt
        - training.feature: Feature file generated from the training corpus
        - test.feature: Feature file generated from the test corpus
        - model.chunk: Trained MaxEnt model
        - response.chunk: System output for development or test corpus

Setup and Execution (*java commands for Windows)
    1. Generate training and test features:
        Command: 
            python extract_features.py
        Output: "training.feature" and "test.feature" files
    2. Compile and train the MaxEnt Model
        Commands:
            javac -cp maxent-3.0.0.jar:trove.jar *.java
            java -cp .:maxent-3.0.0.jar:trove.jar MEtrain training.feature model.chunk
    3. Tag the Test Corpus
        Command: 
            java -cp ".;maxent-3.0.0.jar;trove.jar" MEtag test.feature model.chunk response.chunk
    4. Evaluate the system
        Command:
            python score.chunk.py WSJ_CHUNK_FILES\WSJ_24.pos-chunk response.chunk

Performance on Development Corpus:
    Accuracy: 96.83%
    Precision: 90.40%
    Recall: 92.89%
    F1 Score: 91.16%