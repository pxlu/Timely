# -*- coding: utf-8 -*-
# parser.py

import sys
import re
import itertools

ABBREVIATIONS = "../assets/wordlists/abbrev.english"
CONTRACTIONS = {
    "'m", "'ll", "'d", "'ve", "'re"
}
END= "/END"

def _get_abbreviations():
    """
    Gets a list of abbreviations from a file.
    :return: set of abbreviations
    """

    f = open(ABBREVIATIONS)
    abbrev = [x.lower() for x in f.readlines()]
    return set(abbrev)

ABBREVS = _get_abbreviations()

def _clean_text(text):
    """
    Removes all unnecessary marks from tweets.
    :param text: a tweet
    :return: cleaned text
    """

    # space possessive
    cleaned = _space_possessives(text)
    # remove double spaces
    cleaned = re.sub(r'\s\s+', ' ', cleaned)
    return cleaned

def _break_to_sentences(text):
    """
    Breaks up the tweet into sentences.
    :param text: a tweet
    :return: list of sentences
    """
    # Find all words that end with a period
    last_words = set(re.findall(r'\s\w+\.[\s|\n]+\w', text))
    # Goes through the whole tweet and mark all end of sentences with the END tag
    for word in last_words:
        # mark end of sentence when one the following do not happen:
        # 1. it is an abbreviation
        # 2. it is an ellipsis and the start of next word is lower case
        if not (((word[:-2]).lower() + "\n" in ABBREVS) or ((word.endswith(r'\.\.\.+[\s|\n]\w')) and word[-1].islower())):
            text = text.replace(word[:-1], word[:-2] + END)
    # end of sentence for ? and !
    other_ends = set(re.findall(r'[\?|!]+[\s|\n]', text))
    for end in other_ends:
        text = text.replace(end, end[:-1] + END)
    # split up the sentences by END tag
    sentences = re.split(END, text)
    return [sentence.strip() for sentence in sentences]

def _split_punctuation(text):
    """
    Split all the punctuation from the words
    :param text: a tweet
    :return: string of processed tweet
    """
    # return re.sub(r'(\w+)([,:;.?!](?![\w|\|]))', r'\1 \2', text)
    return re.sub(r'(\w+)([`,:;.?!&#<>|+\-=%\(\)\[\]](?![\w|\|]))', r'\1 \2', text)

def _space_possessives(text):
    """
    Add space between base word and 's
    :param text: a tweet
    :return: string of processed tweet
    """
    # Add spaces between the possessives, [x]'s or [xs]'
    text = re.sub(r'([A-z]+[s|S])(\')', r'\1 \2', text)
    return re.sub(r'([A-z]+)(\'[s|S])', r'\1 \2', text)

def _space_contractions(text):
    """
    Add space between contraction base word and contraction
    :param text: a tweet
    :return: string of processed tweet
    """
    found_contradictions = set(re.findall(r'[A-z]+\'[A-z]+', text))
    for word in found_contradictions:
        # extract contraction part
        ending = re.search(r'\'[A-z]+', word).group()
        negative = re.search(r'[N|n]\'[T|t]', word)
        if negative is not None:
            text = text.replace(word, word[:-3] + " " + negative.group())
        elif ending.lower() in CONTRACTIONS:
            text = text.replace(word, word[:-len(ending)] + " " + ending)
    return text

def _fix_sentences(text):
    """
    Processes the text by splitting up by sentences, adding space for possessives and contractions.
    :param text: tweet given
    :return: list of sentences in the tweet
    """
    sentences = _break_to_sentences(text)
    for i in range(len(sentences)):
        sentences[i] = _split_punctuation(sentences[i])
        sentences[i] = _space_possessives(sentences[i])
        sentences[i] = _space_contractions(sentences[i])
    return sentences

def parse_text(in_file, out_file):
    """
    Parse, tokenize, and tag inFile, removing all HTML tags, attributes, links, # from the hashtags and the @ from
    twitter usernames. Each sentence of the tweet is on it's own line and each token is tagged with the appropriate
    part-of-speech and seperated by spaces. Places the result in outFile with a demarcation before each tweet.

    :param in_file: input file
    :param out_file: output file
    :return: None
    """

    # Reminder: need to strip brackets around words

    abbrev = _get_abbreviations()
    word_dict = {}

    # Clean the text and break it down into sentences
    bio_text = in_file.read()
    cleaned_text = _clean_text(bio_text)
    sentences = _fix_sentences(cleaned_text)

    # Break down each sentence into individual words and record their frequency in the word_dict
    for sentence in sentences:
        sentence = sentence.split(" ")
        for word in sentence:
            word = word.lower()
            # Hasn't been seen yet in the word_dict:
            if word not in word_dict:
                word_dict[word] = 1
            # Add one to the total count of the word    
            else:
                word_dict[word] += 1

    return word_dict

if __name__ == "__main__":
    in_file_name = sys.argv[1]
    out_file_name = sys.argv[2]
    in_file = open(in_file_name, 'r')
    with open(out_file_name, 'w') as out_file: 
        parse_text(in_file, out_file)