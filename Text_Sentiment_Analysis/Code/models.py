import torch.nn as nn
import torch.nn.functional as F
import torch
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.modeling_bert import BertEmbeddings, BertEncoder

from config import CNNConfig, RNNConfig, MLPConfig, BERTConfig

class CNN(nn.Module):
    def __init__(self, vocab_size, embedding_matrix=None):
        super().__init__()

        self.embedding_dim = CNNConfig.EMBEDDING_DIM
        self.kernel_sizes = CNNConfig.KERNEL_SIZES
        self.num_filters = CNNConfig.NUM_FILTERS
        self.num_classes = CNNConfig.NUM_CLASSES

        self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
        self.embedding.weight.requires_grad = True
        if embedding_matrix is not None:
            self.embedding.weight.data.copy_(embedding_matrix)
        self.convs = nn.ModuleList([
            nn.Conv2d(1, self.num_filters, (k, self.embedding_dim)) for k in self.kernel_sizes
        ])
        self.fc = nn.Linear(len(self.kernel_sizes) * self.num_filters, self.num_classes)

    def forward(self, x):
        x = self.embedding(x).unsqueeze(1)
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs]
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]
        x = torch.cat(x, 1)
        x = self.fc(x)
        return F.log_softmax(x, dim=1)

    def save_model(self, path):
        torch.save(self.state_dict(), path)

class LSTM(nn.Module):
    def __init__(self, vocab_size, embedding_matrix=None):
        super().__init__()

        self.embedding_dim = RNNConfig.EMBEDDING_DIM
        self.hidden_dim = RNNConfig.HIDDEN_DIM
        self.num_classes = RNNConfig.NUM_CLASSES

        self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
        if embedding_matrix is not None:
            self.embedding.weight.data.copy_(embedding_matrix)
        self.rnn = nn.LSTM(self.embedding_dim, self.hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(self.hidden_dim * 2, self.num_classes)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.rnn(x)
        x = torch.cat((x[:, -1, :self.hidden_dim], x[:, 0, self.hidden_dim:]), dim=1)
        x = self.fc(x)
        return F.log_softmax(x, dim=1)

    def save_model(self, path):
        torch.save(self.state_dict(), path)

class GRU(nn.Module):
    def __init__(self, vocab_size, embedding_matrix=None):
        super().__init__()

        self.embedding_dim = RNNConfig.EMBEDDING_DIM
        self.hidden_dim = RNNConfig.HIDDEN_DIM
        self.num_classes = RNNConfig.NUM_CLASSES

        self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
        if embedding_matrix is not None:
            self.embedding.weight.data.copy_(embedding_matrix)
        self.rnn = nn.GRU(self.embedding_dim, self.hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(self.hidden_dim * 2, self.num_classes)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.rnn(x)
        x = torch.cat((x[:, -1, :self.hidden_dim], x[:, 0, self.hidden_dim:]), dim=1)
        x = self.fc(x)
        return F.log_softmax(x, dim=1)

    def save_model(self, path):
        torch.save(self.state_dict(), path)

class MLP(nn.Module):
    def __init__(self, vocab_size, embedding_matrix=None):
        super().__init__()

        self.embedding_dim = MLPConfig.EMBEDDING_DIM
        self.num_classes = MLPConfig.NUM_CLASSES
        self.hidden_dim = MLPConfig.HIDDEN_DIM

        self.embedding = nn.Embedding(vocab_size, self.embedding_dim)
        if embedding_matrix is not None:
            self.embedding.weight.data.copy_(embedding_matrix)
        self.mlp = nn.Linear(self.embedding_dim, self.hidden_dim)
        self.fc = nn.Linear(self.hidden_dim, self.num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.embedding(x)
        x = torch.mean(x, dim=1)
        x = self.mlp(x)
        x = self.relu(x)
        x = self.fc(x)
        return F.log_softmax(x, dim=1)

    def save_model(self, path):
        torch.save(self.state_dict(), path)

class BERT(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()

        self.config = BertConfig(
            vocab_size = vocab_size,
            hidden_size = BERTConfig.HIDDEN_DIM,
            num_hidden_layers = BERTConfig.NUM_HIDDEN_LAYERS,
            num_attention_heads = BERTConfig.NUM_ATTENTION_HEADS,
            intermediate_size = BERTConfig.INTERMEDIATE_SIZE,
        )

        self.embeddings = BertEmbeddings(self.config)
        self.bert = BertEncoder(self.config)
        self.dropout = nn.Dropout(BERTConfig.DROPOUT)
        self.fc = nn.Linear(BERTConfig.HIDDEN_DIM, BERTConfig.NUM_CLASSES)

    def forward(self, x):
        x = self.embeddings(x)
        x = self.bert(x)[0]
        x = x[:, 0]
        x = self.dropout(x)
        x = self.fc(x)
        return F.log_softmax(x, dim=1)

    def save_model(self, path):
        torch.save(self.state_dict(), path)
