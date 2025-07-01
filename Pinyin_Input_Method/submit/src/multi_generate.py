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

def viterbi(sentence_pinyin, character_table, width, **kwargs):
    candidates_list = []
    candidates = []
    n = len(kwargs.keys())
    weights = {
        'prob1': 1.5,
        'prob2': 1.0,
        'prob3': 0.7,
        'prob4': 0.5
    }

    for word in character_table[sentence_pinyin[0]]:
        candidates.append(Node(word, get_weight(kwargs['prob1'].get(word, 0)), None))

    candidates.sort(key=lambda x: x.weight)
    candidates = candidates[:width]
    candidates_list.append(candidates)

    for i in range(1, len(sentence_pinyin)):
        candidates = []
        for word in character_table[sentence_pinyin[i]]:
            candidates.append(Node(word, float('inf'), None))
        for j in range(len(candidates)):
            curr_node = candidates[j]
            curr_node.weight = float('inf')
            for k in range(len(candidates_list[i-1])):
                prev_node = candidates_list[i-1][k]
                word2 = prev_node.word + curr_node.word
                if i >= 3:
                    word4 = prev_node.prev.prev.word + prev_node.prev.word + prev_node.word + curr_node.word
                if i >= 2:
                    word3 = prev_node.prev.word + prev_node.word + curr_node.word
                if i >= 3 and word4 in kwargs['prob4']:
                    weight = prev_node.weight + get_weight(kwargs['prob4'].get(word4, 0)) * weights['prob4']
                elif i >= 2 and word3 in kwargs['prob3']:
                    weight = prev_node.weight + get_weight(kwargs['prob3'].get(word3, 0)) * weights['prob3']
                elif word2 in kwargs['prob2']:
                    weight = prev_node.weight + get_weight(kwargs['prob2'].get(word2, 0)) * weights['prob2']
                else:
                    weight = prev_node.weight + get_weight(kwargs['prob1'].get(curr_node.word, 0)) * weights['prob1']
                if weight < curr_node.weight:
                    curr_node.weight = weight
                    curr_node.prev = prev_node

        candidates.sort(key=lambda x: x.weight)
        candidates = candidates[:width]
        candidates_list.append(candidates)

    curr_node = min(candidates_list[-1], key=lambda x: x.weight)

    result = [curr_node.word]
    while curr_node.prev:
        curr_node = curr_node.prev
        result.insert(0, curr_node.word)

    return result

def generate(input, character_table, width, **kwargs):
    output = []
    #start_time = time.time()
    #print('Generating sentences...')

    for sentence_pinyin in tqdm.tqdm(input, desc='Generating sentences'):
        sentence_character = viterbi(sentence_pinyin, character_table, width, **kwargs)
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
    parser.add_argument('--width', type=int, required=False, default=64)
    return parser.parse_args()

def main():
    args = read_args()
    prob1 = read_probs(os.path.join(PROBABILITY_DIR, '1gram_prob.json'), encoding=args.encoding)
    prob2 = read_probs(os.path.join(PROBABILITY_DIR, '2gram_prob.json'), encoding=args.encoding)
    prob3 = read_probs(os.path.join(PROBABILITY_DIR, '3gram_prob.json'), encoding=args.encoding)
    prob4 = read_probs(os.path.join(PROBABILITY_DIR, '4gram_prob.json'), encoding=args.encoding)
    character_table = read_character_table(args.table, encoding=args.encoding)
    input = read_input(args.input, encoding=args.encoding)
    output = generate(input, character_table, args.width, prob1=prob1, prob2=prob2, prob3=prob3, prob4=prob4)
    write_output(output, args.output, encoding=args.encoding)

if __name__ == '__main__':
    main()