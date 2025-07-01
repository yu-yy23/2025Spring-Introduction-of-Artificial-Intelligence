import argparse
import os

from config import TrainingConfig as config
from config import path
from train import train

def parse_args():
    parser = argparse.ArgumentParser(description="Train a text classification model")
    parser.add_argument("--model", type=str, choices=["cnn", "lstm", "gru", "mlp", "bert"], required=True)
    parser.add_argument("--batch_size", type=int, default=config.BATCH_SIZE)
    parser.add_argument("--learning_rate", type=float, default=config.LEARNING_RATE)
    parser.add_argument("--num_epochs", type=int, default=config.NUM_EPOCHS)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    os.makedirs(path.MODELS_DIR, exist_ok=True)
    train(
        model_name=args.model,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        num_epochs=args.num_epochs
    )
