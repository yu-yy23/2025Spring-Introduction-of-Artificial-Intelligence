import json
import math

class Node:
    def __init__(self, word, prob, prev):
        self.word = word
        self.prob = prob
        self.prev = prev

m_lambda = 0.98

def read_table():
    with open('1_word.txt', 'r', encoding='utf-8') as f:
        words = json.loads(f.read())

    with open('2_word.txt', 'r', encoding='utf-8') as f:
        word2s = json.loads(f.read())

    return words, word2s

def preprocess_words(words):
    words_frequency = {}
    words_prob = {}
    total_count = 0

    for words_dict in words.values():
        total_count += sum(words_dict['counts'])

    for words_dict in words.values():
        for word, count in zip(words_dict['words'], words_dict['counts']):
            words_frequency[word] = count
            if count > 0:
                words_prob[word] = -math.log(count / total_count)
            else:
                words_prob[word] = float('inf')

    return words_frequency, words_prob

def preprocess_word2s(word2s, words_frequency):
    word2s_prob = {}
    for word2s_dict in word2s.values():

        for word2, count in zip(word2s_dict['words'], word2s_dict['counts']):
            word = word2.split(' ')[0]
            word1_total_count = words_frequency[word]

            if count > 0 and word1_total_count > 0:
                word2s_prob[word2] = -math.log(count / word1_total_count * m_lambda + (1 - m_lambda) * words_frequency.get(word2.split(' ')[1], 0))
            else:
                word2s_prob[word2] = float('inf')

    return word2s_prob

def viterbi(words, words_prob, word2s_prob, sentence_pinyin):
    candidates_list = []
    candidates = []
    for word in words[sentence_pinyin[0]]['words']:
        candidates.append(Node(word, words_prob[word], None))

    candidates_list.append(candidates)

    if len(sentence_pinyin) == 1:
        return [min(candidates_list[0], key=lambda x: x.prob).word]

    for i in range(1, len(sentence_pinyin)):
        candidates = []
        for word in words[sentence_pinyin[i]]['words']:
            candidates.append(Node(word, float('inf'), None))

        for j in range(len(candidates)):
            curr_node = candidates[j]
            for k in range(len(candidates_list[i - 1])):
                prev_node = candidates_list[i - 1][k]
                word2 = prev_node.word + ' ' + curr_node.word
                if word2 in word2s_prob:
                    prob = prev_node.prob + word2s_prob[word2]
                else:
                    if curr_node.word in words_prob:
                        prob = prev_node.prob + words_prob[curr_node.word]
                    else:
                        prob = prev_node.prob + 20

                if prob < curr_node.prob:
                    curr_node.prob = prob
                    curr_node.prev = prev_node

        candidates_list.append(candidates)

    curr_node = min(candidates_list[-1], key=lambda x: x.prob)

    result = [curr_node.word]
    while curr_node.prev:
        curr_node = curr_node.prev
        result.insert(0, curr_node.word)

    return result

def main():
    words, word2s = read_table()
    words_frequency, words_prob = preprocess_words(words)
    word2s_prob = preprocess_word2s(word2s, words_frequency)
    sentence_pinyin = []
    try:
        while True:
            sentence_pinyin = input().strip().split()
            result = viterbi(words, words_prob, word2s_prob, sentence_pinyin)
            print(''.join(result))
    except EOFError:
        pass

if __name__ == '__main__':
    main()