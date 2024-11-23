# Dollar Amount and Telephone Number Extraction Program

This project extracts dollar amounts or telephone numbers from text files using regular expressions.

## dollar_regexp.py:
### Features:
 - extracts dollar amounts including words like million, billion, etc.
 - includes numbers and decimals
 - includes dollar signs, the words "dollar", "dollars", "cent", and "cents"
 - excludes currencies that are not stated in terms of dollars and cents
### Output: 
 - returns each match into the output file "dollar_output.txt", one match per line
### Command: 
     `python dollar_regexp.py <input_file_name>`
     
## telephone_regexp.py:
### Features:
 - handles cases with and without area codes
 - handles different punctuation 
### Output: 
 - returns each match into the output file "telephone_output.txt", one match per line
### Command: 
     `python telephone_regexp.py <input_file_name>`
