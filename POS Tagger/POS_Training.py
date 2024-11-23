import sys
from collections import defaultdict

# To Run:
# python3 POS_Training.py WSJ_02-21.pos WSJ_02-21_Training_Prob.txt 

def train_model(input_file):
    likelihood = defaultdict(lambda: defaultdict(int))
    transitions = defaultdict(lambda: defaultdict(int))
    
    previous_pos = "Begin_S"
    word_set = set()  # track all unique words

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            
            # check for blank line or end of file
            if line == "":
                transitions[previous_pos]['End_S'] += 1
                previous_pos = "Begin_S"  # reset for new sentence
                continue
            
            word, pos = line.split('\t')
            word_set.add(word)

            # update likelihood and transition tables
            likelihood[pos][word] += 1
            transitions[previous_pos][pos] += 1

            # update previous pos for next loop
            previous_pos = pos

    # convert to probabilities
    likelihood_probs = convert_to_prob(likelihood)
    transitions_probs = convert_to_prob(transitions)
    
    return likelihood_probs, transitions_probs, word_set

def convert_to_prob(table):
    # convert frequency table to probability table
    probability_table = defaultdict(dict)
    
    for category, item in table.items():
        total_count = sum(item.values())
        for sub_category, count in item.items():
            probability_table[category][sub_category] = count / total_count

    return probability_table

def write_to_file(output_file, likelihood_probs, transitions_probs):
    with open(output_file, 'w') as file:
        for pos, words_dict in likelihood_probs.items():
            for word, prob in words_dict.items():
                file.write(f"{pos}\t{word}\t{prob:.6f}\n")
        
        file.write("\n")
        for state, next_states_dict in transitions_probs.items():
            for next_state, prob in next_states_dict.items():
                file.write(f"{state}\t{next_state}\t{prob:.6f}\n")

if __name__ == "__main__":
    # make sure argument is correct
    if len(sys.argv) != 3:
        print("Usage: python3 POS_Training_HW3.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # train the model
    likelihood_probs, transitions_probs, word_set = train_model(input_file)

    # write to the output file
    write_to_file(output_file, likelihood_probs, transitions_probs)

    print(f"Training complete. Results saved to {output_file}.")
