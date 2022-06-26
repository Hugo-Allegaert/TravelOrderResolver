from typing import Any
from fastapi import HTTPException


class NaiveBayesService:
    model: Any
    vec: Any

    def __init__(self, model, vec):
        self.model = model
        self.vec = vec

    def predict(self, sentence):
        if self.model.predict(self.vec.transform([sentence]))[0] == 1:
            return sentence
        else:
            raise HTTPException(status_code=403, detail="This is not a travel order")
