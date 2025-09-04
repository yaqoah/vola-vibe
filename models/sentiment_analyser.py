from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

class Financial_Sentiment_Analyser:
    _is_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._is_instance: 
           cls. _is_instance = super().__new__(cls)

        return cls._is_instance

    def __init__(self):
        if not hasattr(self, 'sentiment_pipeline'): 
            model_name = "ProsusAI/finbert"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            device = 0 if torch.cuda.is_available() else -1
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis", model=model, tokenizer=tokenizer, device=device
            )
            print("✅ FinBERT Sentiment Model Loaded.")

    def analyze_sentiment(self, text):
        if not text or not isinstance(text, str):
            return {'label': 'neutral', 'score': 0.0}
        
        results = self.sentiment_pipeline([text])
        return results[0]

    def get_aggregated_score(self, headlines, batch_size=32):
        if not headlines:
            return 0.0

        total_scores = []
        for i in range(0, len(headlines), batch_size):
            batch = headlines[i:i+batch_size]
            results = self.sentiment_pipeline(batch)
            for sentiment in results:
                score = sentiment['score']
                if sentiment['label'] == 'negative':
                    score *= -1
                elif sentiment['label'] == 'neutral':
                    score = 0
                total_scores.append(score)

        return sum(total_scores) / len(total_scores)


sentiment_analyser = Financial_Sentiment_Analyser()