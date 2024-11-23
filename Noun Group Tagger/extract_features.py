def tags_since_dt(sentence, i):
    tags = set()
    for word_pos in sentence[:i]:
        _, pos = word_pos.split()  
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)
    return '+'.join(sorted(tags))

def extract_features(input_file, output_file, is_training=True):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        prev_pos = "<START>"
        prev_tag = "O"  
        lines = f_in.readlines()
        
        sentence = []
        
        for i, line in enumerate(lines):
            if line.strip() == "":
                f_out.write("\n")
                prev_pos = "<START>"
                prev_tag = "O"
                sentence = []
                continue
            
            parts = line.strip().split()
            word = parts[0]
            pos = parts[1]
            bio_tag = parts[2] if is_training else None
            
            sentence.append(f"{word} {pos}")
            
            features = [
                word,
                f"POS={pos}",
                f"CAPITALIZED={'YES' if word[0].isupper() else 'NO'}",
                f"WORD_SHAPE={'UPPER' if word.isupper() else 'LOWER' if word.islower() else 'CAPITALIZED' if word.istitle() else 'MIXED'}",
                f"HAS_DIGIT={'YES' if any(char.isdigit() for char in word) else 'NO'}",
                f"HAS_HYPHEN={'YES' if '-' in word else 'NO'}",
                f"LENGTH={len(word)}",
                f"PREFIX_1={word[:1]}",
                f"PREFIX_2={word[:2]}",
                f"SUFFIX_1={word[-1:]}",
                f"SUFFIX_2={word[-2:]}"
            ]
            
            if i > 0 and lines[i-1].strip():
                prev_parts = lines[i-1].strip().split()
                prev_word = prev_parts[0]
                prev_pos = prev_parts[1]
                features.append(f"PREV_WORD={prev_word}")
                features.append(f"PREV_POS={prev_pos}")
                features.append(f"prevpos+pos={prev_pos}+{pos}")
                if is_training:
                    features.append(f"PREV_BIO={prev_tag}")
            else:
                features.append("PREV_WORD=BOS")
                features.append(f"prevpos+pos=<START>+{pos}")
            
            if i < len(lines) - 1 and lines[i+1].strip():
                next_parts = lines[i+1].strip().split()
                next_word = next_parts[0]
                next_pos = next_parts[1]
                features.append(f"NEXT_WORD={next_word}")
                features.append(f"NEXT_POS={next_pos}")
                features.append(f"pos+nextpos={pos}+{next_pos}")
            else:
                features.append("NEXT_WORD=EOS")
                features.append(f"pos+nextpos={pos}+<END>")
            
            tags_since_dt_feature = tags_since_dt(sentence, len(sentence))
            features.append(f"tags-since-dt={tags_since_dt_feature}")
            
            if i > 1 and lines[i-2].strip():
                prev_prev_parts = lines[i-2].strip().split()
                features.append(f"PREV2_WORD={prev_prev_parts[0]}")
                features.append(f"PREV2_POS={prev_prev_parts[1]}")
            else:
                features.append("PREV2_WORD=BOS")

            if i < len(lines) - 2 and lines[i+2].strip():
                next_next_parts = lines[i+2].strip().split()
                features.append(f"NEXT2_WORD={next_next_parts[0]}")
                features.append(f"NEXT2_POS={next_next_parts[1]}")
            else:
                features.append("NEXT2_WORD=EOS")
            
            if is_training:
                features.append(bio_tag)
                prev_tag = bio_tag
            
            f_out.write("\t".join(features) + "\n")

# Training
extract_features('WSJ_CHUNK_FILES/WSJ_02-21.pos-chunk', 'training.feature', is_training=True)
# Development
extract_features('WSJ_CHUNK_FILES/WSJ_24.pos', 'test.feature', is_training=False)
