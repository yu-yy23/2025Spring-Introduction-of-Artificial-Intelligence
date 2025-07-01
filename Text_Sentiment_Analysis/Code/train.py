import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR
from sklearn.metrics import accuracy_score, f1_score
import wandb

from models import CNN, LSTM, GRU, MLP, BERT
from dataset import TextDataset
from utils import load_word2vec, create_vocab, load_data, texts_to_indices
from config import path, WandbConfig

def train(model_name, batch_size, learning_rate, num_epochs):

    # Get chosen model name
    # model_name = config.MODEL_NAME
    print(f"Model name: {model_name}")

    # Set hyperparameters
    # batch_size = config.BATCH_SIZE
    # learning_rate = config.LEARNING_RATE
    # num_epochs = config.NUM_EPOCHS
    print(f"Batch size: {batch_size}")
    print(f"Learning rate: {learning_rate}")
    print(f"Number of epochs: {num_epochs}")

    # Initialize wandb
    # wandb.init(
    #     entity=WandbConfig.ENTITY,
    #     project=WandbConfig.PROJECT,
    #     config={
    #         "learning_rate": learning_rate,
    #         "architecture": model_name.upper(),
    #         "batch_size": batch_size,
    #         "epochs": num_epochs,
    #     }
    # )

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load data
    print("Starting to load data...")
    word2vec= load_word2vec(path.WORD_VECTOR_MODEL_PATH)
    vocab_size = len(word2vec.key_to_index) + 2
    embedding_dim = word2vec.vector_size
    print(f"Vocabulary size: {vocab_size}\nEmbedding dimension: {embedding_dim}")

    word_to_index, embedding_matrix = create_vocab(word2vec)
    train_data_texts, train_data_labels = load_data(path.TRAIN_DATA_PATH)
    validation_data_texts, validation_data_labels = load_data(path.VALIDATION_DATA_PATH)
    test_data_texts, test_data_labels = load_data(path.TEST_DATA_PATH)
    train_data_indices = texts_to_indices(train_data_texts, word_to_index)
    validation_data_indices = texts_to_indices(validation_data_texts, word_to_index)
    test_data_indices = texts_to_indices(test_data_texts, word_to_index)
    print("Data loaded")

    # Create data loaders
    train_dataset = TextDataset(train_data_indices, train_data_labels)
    validation_dataset = TextDataset(validation_data_indices, validation_data_labels)
    test_dataset = TextDataset(test_data_indices, test_data_labels)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    validation_loader = DataLoader(validation_dataset, batch_size=batch_size)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    # Initialize model
    if model_name == "cnn":
        model = CNN(vocab_size=vocab_size, embedding_matrix=embedding_matrix).to(device)
    elif model_name == "lstm":
        model = LSTM(vocab_size=vocab_size, embedding_matrix=embedding_matrix).to(device)
    elif model_name == "gru":
        model = GRU(vocab_size=vocab_size, embedding_matrix=embedding_matrix).to(device)
    elif model_name == "mlp":
        model = MLP(vocab_size=vocab_size, embedding_matrix=embedding_matrix).to(device)
    elif model_name == "bert":
        model = BERT(vocab_size=vocab_size).to(device)
    else:
        raise ValueError("Invalid model name.")
    print("Model initialized")

    # Define loss function
    loss_fn = nn.CrossEntropyLoss()
    print("Loss function defined")

    # Define optimizer
    # optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    print("Optimizer defined")

    # Start training
    print("Starting training...")

    # scheduler = StepLR(optimizer, step_size=2, gamma=0.5)

    for epoch in range(num_epochs):
        print(f"Epoch [{epoch+1}/{num_epochs}]")

        # Training
        model.train()
        train_loss = 0
        all_preds = []
        all_labels = []

        for batch in train_loader:
            indices, labels = batch
            indices, labels = indices.to(device), labels.to(device)

            # Forward pass
            outputs = model(indices)
            _, preds = torch.max(outputs, 1)

            loss = loss_fn(outputs, labels)
            train_loss += loss.item()

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

        train_loss /= len(train_loader)
        train_accuracy = accuracy_score(all_labels, all_preds)
        train_f1 = f1_score(all_labels, all_preds, average='weighted')

        # scheduler.step()
        print(f"Train")
        print(f"Loss: {train_loss:.4f}, Accuracy: {train_accuracy:.4f}, F1 Score: {train_f1:.4f}")

        # Validation
        model.eval()
        validation_loss = 0
        with torch.no_grad():
            all_preds = []
            all_labels = []
            for batch in validation_loader:
                indices, labels = batch
                indices, labels = indices.to(device), labels.to(device)

                outputs = model(indices)
                _, preds = torch.max(outputs, 1)

                loss = loss_fn(outputs, labels)
                validation_loss += loss.item()

                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

            validation_loss /= len(validation_loader)
            validation_accuracy = accuracy_score(all_labels, all_preds)
            validation_f1 = f1_score(all_labels, all_preds, average='weighted')

            print(f"Validation")
            print(f"Loss: {validation_loss:.4f}, Accuracy: {validation_accuracy:.4f}, F1 Score: {validation_f1:.4f}")

        # Test
        test_loss = 0
        with torch.no_grad():
            all_preds = []
            all_labels = []
            for batch in test_loader:
                indices, labels = batch
                indices, labels = indices.to(device), labels.to(device)

                outputs = model(indices)
                _, preds = torch.max(outputs, 1)

                loss = loss_fn(outputs, labels)
                test_loss += loss.item()

                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

            test_loss /= len(test_loader)
            test_accuracy = accuracy_score(all_labels, all_preds)
            test_f1 = f1_score(all_labels, all_preds, average='weighted')

            print(f"Test")
            print(f"Loss: {test_loss:.4f}, Accuracy: {test_accuracy:.4f}, F1 Score: {test_f1:.4f}")

        # Log metrics to wandb
        # wandb.log({
        #     "epoch": epoch + 1,
        #     "train_loss": train_loss,
        #     "train_accuracy": train_accuracy,
        #     "train_f1": train_f1,
        #     "validation_loss": validation_loss,
        #     "validation_accuracy": validation_accuracy,
        #     "validation_f1": validation_f1,
        #     "test_loss": test_loss,
        #     "test_accuracy": test_accuracy,
        #     "test_f1": test_f1,
        # })

    print("Training completed")

    # Save the model
    model_path = path.MODELS_DIR + f"{model_name}_model.pth"
    model.save_model(model_path)
    print(f"Model saved in {model_path}")
