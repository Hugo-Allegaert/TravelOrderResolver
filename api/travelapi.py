from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import src.services.dijkstra as dijkstra
import spacy
import pandas as pd
import uvicorn
from src.services.resolver_service import ResolverService
from src.models.travel_order import TravelOrder
from src.services.naives_bayes_service import NaiveBayesService
from joblib import load

model = load('src/ressources/naive_bayes_model.joblib')
vec = load('src/ressources/vectorizer.joblib')

nlp = spacy.load('fr_core_news_sm')

french_cities_df = pd.read_csv(r'src/ressources/city_name.csv')
french_cities = french_cities_df.iloc[:, 0].str.lower()

travel_words = ["aller", "voyage", "destination",
                "emmener", "vers", "arriver", "partir"]

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/trip/start_id={start_id}&end_id={end_id}")
def get_trip(start_id: str, end_id: str):
    trips, possible = dijkstra.get_trip(start_id, end_id)
    return {"all_trips": trips, "possible_trips": possible}


@app.get("/stops_info/start_name={start_name}&end_name={end_name}")
def get_stops_info(start_name: str, end_name: str):
    try:
        return {'start': dijkstra.get_stop_info(start_name), 'end': dijkstra.get_stop_info(end_name)}
    except:
        raise HTTPException(
            status_code=404, detail="No stops found")


@app.post("/travel-order")
def resolve_travel_order(travel_order: TravelOrder):
    naive_bayes_service = NaiveBayesService(model, vec)
    naive_bayes_service.predict(travel_order.travel_order)
    resolver_service = ResolverService(nlp, french_cities)
    return resolver_service.find_origin_and_destination(travel_order.travel_order)


if __name__ == "__main__":
    uvicorn.run("travelapi:app", host="127.0.0.1", port=8000, log_level="info")
