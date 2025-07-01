import os
from tqdm import tqdm
from collections import Counter
import json
import argparse

def read_counter(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        counter_dict = json.load(f)
    return Counter(counter_dict)

def read_n_grams(dir, n, encoding='utf-8'):
    gram_counter = Counter()
    #print(f'Reading {n}-grams data from {dir}...')
    for file in tqdm(os.listdir(dir), desc=f'Reading {n}-grams data'):
        if file.endswith(f'_{n}gram.json'):
            gram_counter += read_counter(os.path.join(dir, file), encoding=encoding)

    #print(f'Finished reading {n}-grams data.')
    #print(f'Total {n}-grams: {len(gram_counter)}')
    #print()

    return gram_counter

def process_1_prob(character_counter):
    probs = {}
    total_count = sum(character_counter.values())
    #print(f'Starting to process 1-gram probabilities...')
    for character in tqdm(character_counter, desc='Processing 1-gram probabilities'):
        prob = character_counter.get(character, 0) / total_count
        probs[character] = prob

    #print('Finished processing 1-gram probabilities.')
    #print(f'Total probabilities: {len(probs)}')
    #print()

    return probs

def process_n_prob(counter_n, counter_n_1, n):
    probs = {}
    #print(f'Starting to process {n}-gram probabilities...')
    for gram in tqdm(counter_n, desc='Processing n-gram probabilities'):
        try:
            prob = counter_n.get(gram, 0) / counter_n_1[gram[:-1]]
            probs[gram] = prob
        except:
            pass

    #print(f'Finished processing {n}-gram probabilities.')
    #print(f'Total probabilities: {len(probs)}')
    #print()

    return probs

def write_probs(probabilities, file, encoding='utf-8'):
    with open(file, 'w', encoding=encoding) as f:
        json.dump(probabilities, f, ensure_ascii=False)

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', type=str, required=True)
    parser.add_argument('--encoding', type=str, required=False, default='utf-8')
    parser.add_argument('--outdir', type=str, required=False, default='probability')
    parser.add_argument('--arity', type=int, required=False, default=4)
    return parser.parse_args()

def main():
    args = read_args()
    os.makedirs(args.outdir, exist_ok=True)

    counter_1gram = read_n_grams(args.indir, 1, encoding=args.encoding)
    prob_1gram = process_1_prob(counter_1gram)
    write_probs(prob_1gram, os.path.join(args.outdir, '1gram_prob.json'), encoding=args.encoding)

    if args.arity >= 2:
        counter_2gram = read_n_grams(args.indir, 2, encoding=args.encoding)
        prob_2gram = process_n_prob(counter_2gram, counter_1gram, 2)
        write_probs(prob_2gram, os.path.join(args.outdir, '2gram_prob.json'), encoding=args.encoding)

    if args.arity >= 3:
        counter_3gram = read_n_grams(args.indir, 3, encoding=args.encoding)
        prob_3gram = process_n_prob(counter_3gram, counter_2gram, 3)
        write_probs(prob_3gram, os.path.join(args.outdir, '3gram_prob.json'), encoding=args.encoding)

    if args.arity >= 4:
        counter_4gram = read_n_grams(args.indir, 4, encoding=args.encoding)
        prob_4gram = process_n_prob(counter_4gram, counter_3gram, 4)
        write_probs(prob_4gram, os.path.join(args.outdir, '4gram_prob.json'), encoding=args.encoding)

if __name__ == '__main__':
    main()
