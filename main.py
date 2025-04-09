import argparse
import os
from scripts import train, evaluate, retrain
from utils import monitor


def main():
    parser = argparse.ArgumentParser(description="CVSS Score Prediction Pipeline")
    parser.add_argument("--action", type=str, required=True, help="train | retrain | evaluate | monitor")
    parser.add_argument("--data", type=str, help="Path to dataset (CSV file)")
    parser.add_argument("--threshold", type=float, default=0.95, help="Accuracy threshold for retraining")

    args = parser.parse_args()

    if args.action == "train":
        if args.data:
            train.train_model(args.data)
        else:
            print("Please provide dataset path using --data")

    elif args.action == "evaluate":
        evaluate.evaluate_model()

    elif args.action == "retrain":
        if args.data:
            retrain.retrain_model(args.data)
        else:
            print("Please provide new dataset path using --data")

    elif args.action == "monitor":
        should_retrain = monitor.check_accuracy_threshold(args.threshold)
        if should_retrain:
            print("Accuracy below threshold. Triggering retrain...")
            retrain.retrain_model("data/new_data.csv")
        else:
            print("Accuracy above threshold. No need to retrain.")

    else:
        print("Invalid action. Use train | retrain | evaluate | monitor")


if __name__ == "__main__":
    main()
