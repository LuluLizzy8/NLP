import re
import sys

def extract_telephone_numbers(file):
    with open(file, 'r', encoding='utf=8') as f:
        text = f.read()

    telephone_regex = r'[^0-9\/]((?:\(?\d{3}\)?.?)\d{3}.?\d{4})[^0-9\/]'
    matches = re.findall(telephone_regex, text)

    with open('telephone_output.txt', 'w') as output:
        for match in matches:
            output.write(str(match).strip() + "\n")

if __name__ == "__main__":
    extract_telephone_numbers(sys.argv[1])
