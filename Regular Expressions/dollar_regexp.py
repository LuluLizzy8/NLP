import re
import sys

def extract_dollar_amounts(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()

    dollar_regex = r'(?:[$][0-9\,]+(?:\.[0-9]+)?(?:\s(?:hundred|thousand|million|billion|trillion|gazillion))?)|(?:(?:(?:[0-9]+(?:[0-9\,]+)?(?:\.[0-9]+)?)|one|two|three|four|five|six|seven|eight|nine|ten|tens|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|fourty|fifty|sixty|seventy|eighty|ninety|half|quarter|a)[\s-])+(?:(?:(?:[0-9]+(?:[0-9\,]+)?(?:\.[0-9]+)?)|one|two|three|four|five|six|seven|eight|nine|ten|tens|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|fourty|fifty|sixty|seventy|eighty|ninety|half|quarter|a|of|hundred|hundreds|thousand|thousands|million|millions|billion|billions|trillion|trillions|gazillion)[\s])?+\b(?:dollar|dollars|cent|cents)\b'
    matches = re.findall(dollar_regex, text)

    with open('dollar_output.txt', 'w') as output:
        for match in matches:
            output.write(str(match).strip() + "\n\n")

if __name__ == "__main__":
    extract_dollar_amounts(sys.argv[1])