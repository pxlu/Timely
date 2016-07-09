# -*- coding: utf-8 -*-
# timely_parser.py

# Native
import sys
import re
import requests
import json
import os
from collections import OrderedDict
from nltk.stem.snowball import SnowballStemmer

# Local
import timely_common

# Current working directory
_cwd = os.path.dirname(os.path.realpath(__file__))

CONTRACTIONS = {
    "'m", "'ll", "'d", "'ve", "'re"
}
END= "/END"

KEYWORDS = timely_common._init_keyword_list()
KEYWORDS_NAMES = timely_common._get_keywords(KEYWORDS)

def _get_abbreviations():
    """
    Gets a list of abbreviations from a file.
    :return: set of abbreviations
    """

    f = open(_cwd + "/../assets/wordlists/abbrev.english")
    abbrev = [x.lower() for x in f.readlines()]
    return set(abbrev)

ABBREVS = _get_abbreviations()

def _clean_text(text):
    """
    Removes all unnecessary marks from paragraphs.
    :param text: a paragraph
    :return: cleaned text
    """

    # space possessive
    cleaned = _space_possessives(text)
    # remove double spaces
    cleaned = re.sub(r'\s\s+', ' ', cleaned)
    return cleaned

def _break_to_sentences(text):
    """
    Breaks up the paragraph into sentences.
    :param text: a paragraph
    :return: list of sentences
    """
    # Find all words that end with a period
    last_words = set(re.findall(r'\s\w+\.[\s|\n]+\w', text))
    # Goes through the whole paragraph and mark all end of sentences with the END tag
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
    :param text: a paragraph
    :return: string of processed paragraph
    """
    # return re.sub(r'(\w+)([,:;.?!](?![\w|\|]))', r'\1 \2', text)
    result = re.sub(r'(\w+)([`,:;.?!&#<>|+\-=%\(\)\[\]](?![\w|\|]))', r'\1 \2', text)
    result2 = re.sub(r'(\B[`,:;.?!&#<>|+\-=%\(\)\[\]])(\w+)', r'\1 \2', result)
    return result2

def _space_possessives(text):
    """
    Add space between base word and 's
    :param text: a paragraph
    :return: string of processed paragraph
    """
    # Add spaces between the possessives, [x]'s or [xs]'
    text = re.sub(r'([A-z]+[s|S])(\')', r'\1 \2', text)
    return re.sub(r'([A-z]+)(\'[s|S])', r'\1 \2', text)

def _space_contractions(text):
    """
    Add space between contraction base word and contraction
    :param text: a paragraph
    :return: string of processed paragraph
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
    :param text: paragraph given
    :return: list of sentences in the paragraph
    """
    sentences = _break_to_sentences(text)
    for i in range(len(sentences)):
        sentences[i] = _split_punctuation(sentences[i])
        sentences[i] = _space_possessives(sentences[i])
        sentences[i] = _space_contractions(sentences[i])
    fixed_sentences = _remove_nonwords(sentences)
    return fixed_sentences

def _remove_nonwords(sentence_list):

    fixed = []
    for sentence in sentence_list:
        words = sentence.split(' ')
        for word in words:
            if re.search(r'\B[\\\/`,:;.?!&#<>|+\-=%\(\)\[\]]', word) or re.search(r'(\'s|s\')', word):
                words.remove(word)
        fixed.append(words)

    return fixed

def _stem_conjugations(parsed_words):

    stemmer = SnowballStemmer("english")
    conjugations_list = [[stemmer.stem(word[0]), [word[1], "PRE;" + word[0]]] for word in parsed_words.items()]
    conjugated_words = [word[0] for word in conjugations_list]

    for conjugation in conjugations_list:
        # Conjugations exist in the list
        if conjugated_words.count(conjugation[0]) > 1:
            conjugate_count = 0
            conjugate_indicies = [i for i, j in enumerate(conjugations_list) if j[0] == conjugation[0] and i != conjugations_list.index(conjugation)]
            for conjugate_index in conjugate_indicies:
                conjugate_count += conjugations_list.pop(conjugate_index)[1][0]
            conjugation[1][0] += conjugate_count

    return conjugations_list

def parse_text(in_file):
    """
    Parse and tokenize in_file, and return a OrderedDict of words with their keys being their number of occurences in in_file.

    :param in_file: input file
    :param out_file: output file
    :return: None
    """

    # Clean the text and break it down into sentences
    bio_text = in_file.read()
    cleaned_text = _clean_text(bio_text)
    paragraph = _fix_sentences(cleaned_text)

    # Flatten the list of lists of sentences representing the paragraph
    flat_list = [item.lower() for sublist in paragraph for item in sublist]
    # For each unique word in the paragraph, insert it into an OrderedDict with the key being the word and the value being the number of occurences of that word within the paragraph
    word_dict = {item: flat_list.count(item) for item in flat_list}
    
    matched_words = _stem_conjugations(word_dict)
    sorted_words = sorted(matched_words, key=lambda item: item[0])

    return sorted_words
    
if __name__ == "__main__":
    in_file_name = sys.argv[1]
    in_file = open(in_file_name, 'r')
    parse_text(in_file)