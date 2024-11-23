import sys
from collections import defaultdict

def load_likelihood_transition(filename):
    likelihood = defaultdict(lambda: defaultdict(float))
    transitions = defaultdict(lambda: defaultdict(float))

    with open(filename, 'r') as f:
        lines = f.readlines()

    likelihood_part = True
    for line in lines:
        line = line.strip()
        if not line:
            likelihood_part = False
            continue

        if likelihood_part:
            pos, word, prob = line.split()
            likelihood[pos][word] = float(prob)
        else:
            state, next_state, prob = line.split()
            transitions[state][next_state] = float(prob)

    return likelihood, transitions

def load_words(file_name):
    with open(file_name, 'r') as f:
        return [line.strip() for line in f.readlines()]

def viterbi_algorithm(tokens, states, transitions, likelihood, output_file):
    n = len(tokens)
    viterbi_table = defaultdict(lambda: defaultdict(float))
    backpointer = defaultdict(lambda: defaultdict(str))

    # initialize for first token
    for s in states:
        if 'Begin_S' in transitions and s in transitions['Begin_S']:
            viterbi_table[0][s] = transitions['Begin_S'][s] * likelihood[s].get(tokens[0], 0.0000001)
            backpointer[0][s] = 'Begin_S'

    # fill Viterbi table
    for t in range(1, n):
        for s in states:
            max_score = float('-inf')
            best_prev_state = None
            for s_prev in states:
                if s in transitions[s_prev]:
                    score = (viterbi_table[t-1][s_prev] *
                             transitions[s_prev][s] *
                             likelihood[s].get(tokens[t], 0.0000001))
                    if score > max_score:
                        max_score = score
                        best_prev_state = s_prev
            viterbi_table[t][s] = max_score
            backpointer[t][s] = best_prev_state

    # end of sentence
    max_final_score = float('-inf')
    best_final_state = None
    for s in states:
        if 'End_S' in transitions[s]:
            score = viterbi_table[n-1][s] * transitions[s]['End_S']
            if score > max_final_score:
                max_final_score = score
                best_final_state = s
    viterbi_table[n]['End_S'] = max_final_score
    backpointer[n]['End_S'] = best_final_state

    # backtrack to get best sequence
    best_sequence = []
    current_state = 'End_S'
    for t in range(n, 0, -1):
        current_state = backpointer[t][current_state]
        best_sequence.insert(0, current_state)

    # write results for this sentence to output file
    with open(output_file, 'a') as f:
        for word, pos in zip(tokens, best_sequence):
            f.write(f"{word}\t{pos}\n")
        f.write("\n")

def main(likelihood_transition_file, words_file):
    likelihood, transitions = load_likelihood_transition(likelihood_transition_file)
    states = list(likelihood.keys())

    # load words from the input file
    words = load_words(words_file)

    sentence = []
    output_file = "output.pos"

    open(output_file, 'w').close()

    for word in words:
        if word == "":  #end of sentence
            if sentence:
                viterbi_algorithm(sentence, states, transitions, likelihood, output_file)
                sentence = []
        else:
            sentence.append(word)

    # process the last sentence in case the file doesn't end with a blank line
    if sentence:
        viterbi_algorithm(sentence, states, transitions, likelihood, output_file)

    print(f"POS tagging complete. Results saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python POS_Tagging.py <likelihood_transition_file> <words_file>")
        sys.exit(1)

    likelihood_transition_file = sys.argv[1]
    words_file = sys.argv[2]

    main(likelihood_transition_file, words_file)
