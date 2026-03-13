# this file hadels all the things for the model
import json
import re 

def main(text):

    # lowercase text
    text  = text.lower()

    # preprocess text 
    processed_text = re.sub(r'[^a-zA-Z0-9/s]' , '' , text)

    # Tokenization part 
    tokenised_list = [word for word in processed_text]

    # load the data from the jsonl file learnedWords.jsonl
    word_data = {}
    with open(r'learnedWords.jsonl' , 'r') as file:
        for line in file:
            data = json.loads(line)
            word_data.update(data)

    # make it a dict with index , isExits deafault False
    text_dict = {}
    for index , word in enumerate(tokenised_list):
        text_dict[index] = (word , False)

    # check if word exits in the word_data if True change the value and isExits to True
    