import torch
from torch.utils.data import Dataset

class TextDataset(Dataset):
    def __init__(self, indices, labels):
        self.indices = torch.tensor(indices, dtype=torch.long)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.indices[idx], self.labels[idx]
