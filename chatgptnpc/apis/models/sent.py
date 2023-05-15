import torch
from transformers import (
    AutoTokenizer,
    RobertaForSequenceClassification
)

def load_model(model_name):
    device = torch.device("mps")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = RobertaForSequenceClassification.from_pretrained(model_name).eval()
    model.to(device)
    return tokenizer, model

def predict(inputs, tokenizer, model):
    device = torch.device("mps")
    inputs = tokenizer(inputs, return_tensors="pt").to(device)
    print(f"aaa : {inputs}")
    outputs = model(**inputs)
    logits = outputs.logits.detach().cpu().numpy()
    predicted_class_idx = logits.argmax(axis=-1)
    predicted_sentiment = model.config.id2label[predicted_class_idx[0]]
    return predicted_sentiment