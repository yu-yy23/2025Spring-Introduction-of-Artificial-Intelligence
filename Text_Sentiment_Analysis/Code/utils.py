import numpy as np
import gensim
import torch

from config import DatasetConfig as config

def load_word2vec(path):
    print(f"Loading Word2Vec model from path: {path} ...")
    word2vec = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    print("Word2Vec model loaded")
    return word2vec

def create_vocab(word2vec):
    print("Creating vocabulary...")
    vocab_size = len(word2vec.key_to_index) + 2
    embedding_dim = word2vec.vector_size
    word_to_index = {word: idx + 2 for idx, word in enumerate(word2vec.key_to_index)}
    word_to_index["<PAD>"] = config.PAD_INDEX
    word_to_index["<UNK>"] = config.UNK_INDEX
    embedding_matrix = np.zeros((vocab_size, embedding_dim))
    embedding_matrix[config.PAD_INDEX] = np.zeros(embedding_dim)
    embedding_matrix[config.UNK_INDEX] = np.random.uniform(-0.5, 0.5, embedding_dim)
    for word, idx in word_to_index.items():
        if word in word2vec.key_to_index:
            embedding_matrix[idx] = word2vec[word]
        else:
            embedding_matrix[idx] = np.random.uniform(-0.5, 0.5, embedding_dim)
    print("Vocabulary created")
    return word_to_index, torch.tensor(embedding_matrix)

def load_data(path):
    print(f"Loading data from path: {path} ...")
    texts, labels = [], []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            label, text = line.strip().split('\t')
            labels.append(int(label))
            texts.append(text.split())
    print("Data loaded")
    return texts, labels

def texts_to_indices(texts, word_to_index):
    print("Converting texts to indices...")
    indices = []
    for text in texts:
        indices.append([word_to_index.get(word, word_to_index["<UNK>"]) for word in text])
        while len(indices[-1]) < config.MAX_SEQ_LENGTH:
            indices[-1].append(word_to_index["<PAD>"])
        while len(indices[-1]) > config.MAX_SEQ_LENGTH:
            indices[-1].pop()
    print("Texts converted to indices")
    return np.array(indices)
    # return indices
