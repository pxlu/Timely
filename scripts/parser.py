# -*- coding: utf-8 -*-
# parser.py

import sys
import re
import requests
import json
import common
from collections import OrderedDict

ABBREVIATIONS = "../assets/wordlists/abbrev.english"
CONTRACTIONS = {
    "'m", "'ll", "'d", "'ve", "'re"
}
END= "/END"

KEYWORDS = common._init_keywords_list()
KEYWORDS_NAMES = common._get_keywords(KEYWORDS)

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

def _match_conjunctions(parsed_words, base_match=True):

    # NEED NLP TAGGER TO GET THE POST OF THE WORDS, ONLY WANT WORDS TO BE USED FOR THIS SERVICE IF IT'S A ADJECTIVE TO BEGIN WITH.

    add_dict = {}
    replace_set = set()
    keep_set = set()
    remove_set = set()

    for word in parsed_words.keys():
        # For each word in parsed words, look up words that are similar to it
        requestURL = 'http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=' + word
        request = requests.get(requestURL)
        numresults = request.json()['count']

        # For each word that is similar, add it to the conjugations_set, including itself
        conjugations_set = set()
        for i in range(numresults):
            headword = request.json()['results'][i]['headword']
            conjugations_set.add(headword) 

        # If the word is not in KEYWORDS but it's conjugation is, means that the word is actually a conjugation of the base word
        for conjugation in conjugations_set:
            # If conjugation in KEYWORDS, add it to keep_set
            if conjugation in KEYWORDS_NAMES:
                keep_set.add(conjugation)
            # If word !in KEYWORDS but a conjugation is, add replace word with conjugation, impossible if same word
            if conjugation in KEYWORDS_NAMES and word not in KEYWORDS_NAMES:
                replace_set.add((word, conjugation))
            # If neither in KEYWORDS, remove the latter one
            if word not in KEYWORDS_NAMES and conjugation in parsed_words.keys() and word != conjugation and word not in remove_set:
                remove_set.add(conjugation)

        # Now, collect like terms and group all their counts together
        conjugate_count = 0
        for conjugate in conjugations_set:
            # If the conjugate exists in parsed_words, means that they should be grouped together
            if conjugate != word and conjugate in parsed_words.keys():
                conjugate_count += parsed_words[conjugate]

        # Add it to add_dict so it can be added to the count in parsed_words later
        add_dict[word] = conjugate_count

    for word in parsed_words.keys():
        parsed_words[word] += add_dict[word]

    for pair in replace_set:
        parsed_words[pair[1]] = parsed_words[pair[0]]
        del parsed_words[pair[0]]

    for word in remove_set:
        if word in parsed_words and word not in keep_set:
            del parsed_words[word]

    return parsed_words

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
    
    matched_words = _match_conjunctions(word_dict)
    sorted_words = OrderedDict(sorted(matched_words.items(), key=lambda name: name[0]))

    return sorted_words
    
if __name__ == "__main__":
    in_file_name = sys.argv[1]
    in_file = open(in_file_name, 'r')
    parse_text(in_file)