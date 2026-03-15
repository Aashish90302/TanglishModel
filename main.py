# this file hadels all the things for the model
import json
import re 
from transformers import AutoTokenizer , AutoModelForSeq2SeqLM
import regex 

# ------------------------------------------------------------------------------


# intialization area

# translation intializers
checkpoint = "codeboosterstech/EN-TA"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# open the data file chunkData.json and update into chunk_data={}
with open(r'chunkData.json' , 'r') as file:
    chunk_data = json.load(file)

# ------------------------------------------------------------------------------


# functions 

# add the new word
def AddToData(key,value):
    # this function add the new word to the dataset learnedWords.jsonl
    with open(r'learnedWords.jsonl', 'a') as file:
        data = {key:value}
        file.write(json.dumps(data) + '\n')



# split tamil word
def splitTamilWord(word):   
    # this splits the word graphemeily 
    letters = regex.findall(r'\X', word) 
    return letters

# ------------------------------------------------------------------------------

# translate function
def translate(word):
    # this translates the given word from english to tamil
    tokenized = tokenizer([word], return_tensors='pt')
    out = model.generate(**tokenized, max_length=128)
    return tokenizer.decode(out[0],skip_special_tokens=True)

# ------------------------------------------------------------------------------

# transliterate function 
def transliterate_word(chunkList):
    # this transliterates the given word from tamil to tanglish
    out = []
    # check for each letter and transliterate
    for chunk in chunkList:
        if chunk == ' ':
            out.append(chunk) 
            continue
        
        out.append(chunk_data.get(chunk,chunk))
    
    return ''.join(out)

# ------------------------------------------------------------------------------

# process word
def process_word(word):
    
    # stage- 1 --> translate the word using translate()
    out = translate(word)

    # stage- 2 --> split the tamil word graphemeily using splitTamilWord()
    out = splitTamilWord(out)

    # stage- 3 --> transliterate the splitted tamilchunk  using transliterate_word()
    out = transliterate_word(out)

    # return the final out 
    return ''.join(out)


# ------------------------------------------------------------------------------
# --------------------------- MAIN lOOP ----------------------------------------
# ------------------------------------------------------------------------------

# Main loop
def main(text):

    # lowercase text
    text  = text.lower()

    # preprocess text 
    processed_text = re.sub(r'[^a-zA-Z0-9\s]' , '' , text)

    # Tokenization part 
    tokenised_list = processed_text.split()

    # load the data from the jsonl file learnedWords.jsonl
    word_data = {}
    with open(r'learnedWords.jsonl' , 'r') as file:
        for line in file:
            data = json.loads(line)
            word_data.update(data)

    # make it a list 
    result_words = []

    # loop the tokenised_list 
    for word in tokenised_list:
        # check if word exits in the word_data 
        if word in word_data:
            word = word_data[word]
        
        else:  # fall back keep the same word there and send to process_word()
            new_word = process_word(word)
            # add to the learned data to the  jsonl file leanedWords.jsonl
            AddToData(word,new_word)
            word = new_word

        
        # finallly append the word
        result_words.append(word)
    
    return ' '.join(result_words)

