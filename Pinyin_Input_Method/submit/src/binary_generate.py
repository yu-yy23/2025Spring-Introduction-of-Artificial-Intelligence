import argparse
import json
import math
import tqdm
import time
import os
from settings import PROBABILITY_DIR, PINYIN_CHAR_TABLE_UTF8_FILE, INPUT_FILE, OUTPUT_FILE

class Node:
    def __init__(self, word, weight, prev):
        self.word = word
        self.weight = weight
        self.prev = prev

def read_probs(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        probs = json.load(f)
    return probs

def read_input(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    pinyin = []
    for line in lines:
        pinyin.append(line.split())

    return pinyin

def read_character_table(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    character_table = {}
    for line in lines:
        characters = line.split()
        key = characters[0]
        value = characters[1:]
        character_table[key] = value

    return character_table

def get_weight(prob):
    if prob > 0:
        return -math.log(prob)
    return 20

def viterbi(sentence_pinyin, character_table, **kwargs):
    candidates_list = []
    candidates = []

    for word in character_table[sentence_pinyin[0]]:
        candidates.append(Node(word, get_weight(kwargs['prob1'].get(word, 0)), None))
    candidates_list.append(candidates)

    for i in range(1, len(sentence_pinyin)):
        candidates = []
        for word in character_table[sentence_pinyin[i]]:
            candidates.append(Node(word, float('inf'), None))

        for j in range(len(candidates)):
            curr_node = candidates[j]
            for k in range(len(candidates_list[i-1])):
                prev_node = candidates_list[i-1][k]
                word2 = prev_node.word + curr_node.word
                if word2 in kwargs['prob2']:
                    weight = prev_node.weight + get_weight(kwargs['prob2'].get(word2, 0))
                else:
                    weight = prev_node.weight + get_weight(kwargs['prob1'].get(curr_node.word, 0)) + 2
                if weight < curr_node.weight:
                    curr_node.weight = weight
                    curr_node.prev = prev_node

        candidates_list.append(candidates)

    curr_node = min(candidates_list[-1], key=lambda x: x.weight)

    result = [curr_node.word]
    while curr_node.prev:
        curr_node = curr_node.prev
        result.insert(0, curr_node.word)

    return result

def generate(input, character_table, **kwargs):
    output = []
    #start_time = time.time()
    #print('Generating sentences...')

    for sentence_pinyin in tqdm.tqdm(input, desc='Generating sentences'):
        sentence_character = viterbi(sentence_pinyin, character_table, **kwargs)
        sentence = ''.join(sentence_character)
        output.append(sentence)

    #end_time = time.time()
    #print('Generating sentences completed.')
    #print(f'Generation time: {(end_time - start_time):.2f} seconds')

    return output

def write_output(output, file, encoding='utf-8'):
    with open(file, 'w', encoding=encoding) as f:
        for sentence in output:
            f.write(str(sentence))
            f.write('\n')

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', type=str, required=False, default=PINYIN_CHAR_TABLE_UTF8_FILE)
    parser.add_argument('--input', type=str, required=False, default=INPUT_FILE)
    parser.add_argument('--output', type=str, required=False, default=OUTPUT_FILE)
    parser.add_argument('--encoding', type=str, required=False, default='utf-8')
    return parser.parse_args()

def main():
    args = read_args()
    prob1 = read_probs(os.path.join(PROBABILITY_DIR, '1gram_prob.json'), encoding=args.encoding)
    prob2 = read_probs(os.path.join(PROBABILITY_DIR, '2gram_prob.json'), encoding=args.encoding)
    character_table = read_character_table(args.table, encoding=args.encoding)
    input = read_input(args.input, encoding=args.encoding)

    output = generate(input, character_table, prob1=prob1, prob2=prob2)
    write_output(output, args.output, encoding=args.encoding)

if __name__ == '__main__':
    main()