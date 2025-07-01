class path:
    WORD_VECTOR_MODEL_PATH = "../Dataset/wiki_word2vec_50.bin"
    TRAIN_DATA_PATH = "../Dataset/train.txt"
    VALIDATION_DATA_PATH = "../Dataset/validation.txt"
    TEST_DATA_PATH = "../Dataset/test.txt"
    MODELS_DIR = "../Models/"

class WandbConfig:
    ENTITY = ""                 # Wandb entity
    PROJECT = ""                # Wandb project name

class DatasetConfig:
    MAX_SEQ_LENGTH = 100        # Maximum sequence length for padding
    PAD_INDEX = 0               # Padding index for sequences
    UNK_INDEX = 1               # Unknown index for out-of-vocabulary words

# Model hyperparameters
class TrainingConfig:
    MODEL_NAME = ""             # Model name
    BATCH_SIZE = 64             # Batch size for training
    LEARNING_RATE = 1e-3        # Learning rate for the optimizer
    NUM_EPOCHS = 10             # Number of epochs for training

# CNN hyperparameters
class CNNConfig:
    EMBEDDING_DIM = 50          # Embedding dimension
    NUM_CLASSES = 2             # Number of classes for classification
    KERNEL_SIZES = [2, 3, 4, 5] # Sizes of the convolutional kernels
    NUM_FILTERS = 100           # Number of filters for each kernel size
    DROPOUT = 0.5               # Dropout rate for regularization

# RNN hyperparameters
class RNNConfig:
    EMBEDDING_DIM = 50          # Embedding dimension
    HIDDEN_DIM = 100            # Hidden dimension for the RNN
    NUM_CLASSES = 2             # Number of classes for classification
    DROPOUT = 0.5               # Dropout rate for regularization

# MLP hyperparameters
class MLPConfig:
    EMBEDDING_DIM = 50          # Embedding dimension
    HIDDEN_DIM = 128            # First hidden dimension
    NUM_CLASSES = 2             # Number of classes for classification
    DROPOUT = 0.5               # Dropout rate for regularization

class BERTConfig:
    NUM_CLASSES = 2             # Number of classes for classification
    HIDDEN_DIM = 50             # Hidden dimension for the BERT model
    DROPOUT = 0.5               # Dropout rate for regularization
    NUM_HIDDEN_LAYERS = 1       # Number of hidden layers in the BERT model
    NUM_ATTENTION_HEADS = 1     # Number of attention heads in the BERT model
    INTERMEDIATE_SIZE = 200     # Size of the intermediate layer in the BERT model
