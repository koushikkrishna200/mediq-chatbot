import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def fine_tune_biogpt(model_name="microsoft/biogpt", train_file="path/to/your/train_data.csv", val_file="path/to/your/val_data.csv", output_dir="./biogpt_finetuned"):
    try:
        # Load the pre-trained BioGPT model and tokenizer
        logging.info(f"Loading model: {model_name}")
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Load your custom dataset (adjust dataset location or method)
        logging.info(f"Loading dataset from {train_file} and {val_file}")
        dataset = load_dataset("csv", data_files={"train": train_file, "validation": val_file})

        # Preprocess the dataset
        def preprocess_function(examples):
            return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

        tokenized_datasets = dataset.map(preprocess_function, batched=True)

        # Set up the training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,  # where the model checkpoints will be saved
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=3,
            weight_decay=0.01,
            logging_dir="./logs",
            push_to_hub=False,
            load_best_model_at_end=True,
            logging_steps=100,  # Log every 100 steps
            save_steps=500,     # Save the model every 500 steps
        )

        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["validation"],
            tokenizer=tokenizer,
        )

        # Start the fine-tuning process
        logging.info("Fine-tuning started...")
        trainer.train()

        # Save the fine-tuned model
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)

        logging.info("Fine-tuning completed and model saved!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    fine_tune_biogpt()
