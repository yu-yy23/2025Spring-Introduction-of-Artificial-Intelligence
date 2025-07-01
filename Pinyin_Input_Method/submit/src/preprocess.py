from collections import Counter
import json
import argparse
from tqdm import tqdm
import os
from settings import CHAR_TABLE_UTF8_FILE

def read_character_table(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    characters = set(''.join(lines))
    return characters

def read_sentences(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]

    sentences = []
    for line in lines:
        line = json.loads(line)
        html = line['html']
        if html[:3] == '原标题':
            html = html[:4]
        sentences.append(html)
        sentences.append(line['title'])

    return sentences

def preprocess_grams(sentences, allowed_characters, restricted_words, word_len):
    multi_grams = []
    word = []
    for sentence in tqdm(sentences, desc=f'Preprocessing {word_len}-grams'):
        for character in sentence:
            if character in restricted_words or character not in allowed_characters:
                word = []
                continue
            word.append(character)
            if len(word) == word_len:
                multi_grams.append(''.join(word))
                word = word[1:]

    gram_counter = Counter(multi_grams)
    return gram_counter

def write_counter(counter, file, encoding='utf-8'):
    counter_dict = dict(counter)
    with open(file, 'w', encoding=encoding) as f:
        json.dump(counter_dict, f, ensure_ascii=False)

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--encoding', type=str, required=False, default='utf-8')
    parser.add_argument('--outdir', type=str, required=False, default='frequency_counter')
    parser.add_argument('--arity', type=int, required=False, default=4)
    return parser.parse_args()

def main():
    punctuation = set('，。！？、；：“”‘’（）《》【】\\ :——()….~|｜[]')
    alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    number = set('0123456789')
    restricted_words = punctuation | alphabet | number

    args = read_args()
    input_file = args.input.split('/')[-1].split('.')[0]
    os.makedirs(args.outdir, exist_ok=True)

    allowed_characters_file = CHAR_TABLE_UTF8_FILE
    allowed_characters = read_character_table(allowed_characters_file, args.encoding)

    sentences = read_sentences(args.input, args.encoding)

    for i in range(1, args.arity + 1):
        n_gram_file = args.outdir + '/' + input_file + f'_{i}gram.json'
        n_gram_counter = preprocess_grams(sentences, allowed_characters, restricted_words, i)
        write_counter(n_gram_counter, n_gram_file)

if __name__ == '__main__':
    main()
