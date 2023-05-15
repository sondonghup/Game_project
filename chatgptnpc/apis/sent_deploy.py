import uvicorn
import json
from fastapi import FastAPI
from pydantic import BaseModel
from argparse import ArgumentParser
from models.sent import(
    load_model,
    predict
)

app = FastAPI(
    title = 'kor sent'
)

class SentimentInput(BaseModel):
    text: str

class SentimentOutput(BaseModel):
    sentiment: str

@app.post("/sent", response_model=SentimentOutput)
async def predict_sentiment(input: SentimentInput):
    text = input.text
    result = predict(inputs= text, tokenizer=tokenizers, model=models)
    return SentimentOutput(sentiment=result)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/v0.0.1-sent.json")
    parse = parser.parse_args()
    config_path = parse.config
    config = json.load(open(config_path, encoding='utf-8'))

    tokenizers, models = load_model(config['sent']['model_name'])
    print("[=!=]sent model loaded[=!=]")
    print(models.config.id2label)
    uvicorn.run(app, host="0.0.0.0", port=config['deploy_port'])