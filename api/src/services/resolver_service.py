import difflib
from typing import List

from fastapi import HTTPException
from spacy import Language

prefix_origin_words = ["de", "depuis", "du"]
prefix_destination_words = ["à", "a", "au", "vers", "-", "jusque", "jusqu'à", "jusqu'a"]
prefix_words = prefix_origin_words + prefix_destination_words
wrong_prefix_words = ["le", "la", "du", "de"]
travel_words = ["aller", "voyage", "destination", "emmener", "vers", "arriver", "partir"]


class ResolverService:
    nlp: Language
    french_cities: List[str]

    def __init__(self, nlp, french_cities):
        self.nlp = nlp
        self.french_cities = french_cities

    def clean_text(self, text: str):
        text = text.strip(".")
        text = text.replace(",", "")
        text = text.strip("?")
        # text = text.replace("'", " ")
        return text.lower()

    def split_text(self, text: str):
        text = self.clean_text(text)
        return text.split(" ")

    def is_before(self, text: str, first_words: List[str], second_word: str):

        text_split = self.split_text(text)

        list_result = []

        for first_word in first_words:

            if first_word not in text_split or (second_word not in text_split and second_word not in text):
                list_result.append(False)
            else:

                first_result = False
                second_result = False
                third_result = False

                first_word_index = text_split.index(first_word)

                if second_word in text_split:

                    second_word_index = text_split.index(second_word)

                    if text_split.count(first_word) > 1 and text_split[second_word_index - 1] == first_word:
                        first_word_index = second_word_index - 1

                    first_result = second_word_index - first_word_index == 1

                    if not first_result:
                        prefix = text_split[second_word_index - 1]

                        if prefix == "la" or prefix == "le" or prefix == "l'":
                            prefix_index = text_split.index(prefix)
                            second_result = prefix_index - first_word_index == 1

                if (not first_result or not second_result) and (second_word not in text_split and second_word in text):
                    second_word_split = []

                    if len(second_word.split(" ")) > 1:
                        second_word_split = second_word.split(" ")
                    if len(second_word.split("-")) > 1:
                        second_word_split = second_word.split("-")

                    if second_word_split and second_word_split[0] in text_split:
                        second_word_first_word_index = text_split.index(second_word_split[0])
                        third_result = second_word_first_word_index - first_word_index == 1

                list_result.append(first_result or second_result or third_result)

        return any(result for result in list_result)

    def clean_city(self, city: str):
        city = city.replace("la ", "")
        city = city.replace("le ", "")
        city = city.replace("l' ", "")
        return city.strip()

    def find_origin_and_destination(self, text: str):

        doc = self.nlp(text)

        text_cities = []
        text_travel_words = []
        locations = []

        for ent in doc.ents:
            if ent.text.lower() not in wrong_prefix_words:
                locations.append(self.clean_text(ent.text.lower()))
            text_cities.extend(
                [french_city for french_city in self.french_cities if french_city.startswith(self.clean_text(ent.text))
                 or self.clean_text(ent.text) in french_city
                 or french_city.startswith(self.clean_text(ent.text).replace(" ", "-"))
                 or self.clean_text(ent.text).replace(" ", "-") in french_city])
            if len(ent.text.split(" ")) > 1 and not text_cities:
                for word in ent.text.split(" "):
                    text_cities.extend(
                        [french_city for french_city in self.french_cities if
                         french_city.startswith(self.clean_text(word))
                         or self.clean_text(word) in french_city
                         or french_city.startswith(self.clean_text(word).replace(" ", "-"))
                         or self.clean_text(word).replace(" ", "-") in french_city])

        for token in doc:
            if any(token.lemma_ == travel_word for travel_word in travel_words):
                text_travel_words.append(token.text)

        text_split = self.split_text(text)

        if len(locations) <= 1:
            if len(list(set(text_split).intersection(prefix_origin_words))) > 0 and len(
                    list(set(text_split).intersection(prefix_destination_words))) > 0:
                for index, word in enumerate(text_split):
                    if word in prefix_words:
                        if len(text_split) > index + 1:
                            if text_split[index + 1] in wrong_prefix_words and len(text_split) > index + 2:
                                locations.append(text_split[index + 2])
                            else:
                                locations.append(text_split[index + 1])
                for location in locations:
                    text_cities.extend([french_city for french_city in self.french_cities if
                                        french_city.startswith(self.clean_text(location)) or self.clean_text(
                                            location) in french_city])
        if len(locations) <= 1:
            temp_text = text[0].lower() + text[1:]
            temp_text_split = temp_text.split(" ")
            for tts in temp_text_split:
                if tts[0] == tts[0].upper() and self.clean_text(tts) not in locations:
                    locations.append(self.clean_text(tts))
                    text_cities.extend([french_city for french_city in self.french_cities if
                                        french_city.startswith(self.clean_text(tts)) or self.clean_text(
                                            tts) in french_city])
            if len(locations) == 2 and self.is_before(self.clean_text(text), [locations[1]], locations[0]):
                locations.reverse()

        locations = list(dict.fromkeys(locations))
        text_cities = list(dict.fromkeys(text_cities))
        text_travel_words = list(dict.fromkeys(text_travel_words))

        origins = []
        destinations = []

        for location in locations:

            if len(list(set(text_split).intersection(prefix_origin_words))) > 0 and len(
                    list(set(text_split).intersection(prefix_destination_words))) > 0:
                if self.is_before(self.clean_text(text), prefix_origin_words, self.clean_city(location)):
                    origins.extend([text_city for text_city in text_cities if
                                    self.clean_city(text_city).startswith(location) or self.clean_city(
                                        text_city).startswith(
                                        location.replace(" ", "-"))])
                if self.is_before(self.clean_text(text), prefix_destination_words, self.clean_city(location)):
                    destinations.extend([text_city for text_city in text_cities if
                                         self.clean_city(text_city).startswith(location) or self.clean_city(
                                             text_city).startswith(
                                             location.replace(" ", "-"))])

        if not origins and not destinations and len(locations[0].split(" ")) > 1:
            if self.is_before(self.clean_text(text), [self.clean_city(locations[0].split(" ")[0])],
                              self.clean_city(locations[0].split(" ")[1])):
                origins.extend([text_city for text_city in text_cities if
                                self.clean_city(text_city).startswith(locations[0].split(" ")[0])])
                destinations.extend([text_city for text_city in text_cities if
                                     self.clean_city(text_city).startswith(locations[0].split(" ")[1])])

        if not origins and not destinations and len(locations) == 2:
            if (len(list(set(text_split).intersection(prefix_origin_words))) > 0 or len(
                    list(set(text_split).intersection(prefix_destination_words))) > 0) and text_split.count(
                "à") < 2 and text_split.count("a") < 2:
                for location in locations:
                    if self.is_before(self.clean_text(text), prefix_origin_words, self.clean_city(location)):
                        # print("3.1.1")
                        origins.extend([text_city for text_city in text_cities if
                                        self.clean_city(text_city).startswith(location) or self.clean_city(
                                            text_city).startswith(
                                            location.replace(" ", "-"))])
                    if self.is_before(self.clean_text(text), prefix_destination_words, self.clean_city(location)):
                        # print("3.1.2")
                        destinations.extend([text_city for text_city in text_cities if
                                             self.clean_city(text_city).startswith(location) or self.clean_city(
                                                 text_city).startswith(location.replace(" ", "-"))])
            else:
                # print("3.2")
                for travel_word in text_travel_words:
                    city = locations[0]
                    if len(locations[0].split(" ")) > 1:
                        city = locations[0].split(" ")[0]
                    if travel_word in text_split and self.clean_city(city) in text_split and (
                            text_split.index(travel_word) > text_split.index(self.clean_city(city))):
                        origins.extend([text_city for text_city in text_cities if
                                        text_city.startswith(locations[0]) or text_city.startswith(
                                            locations[0].replace(" ", "-"))])
                        destinations.extend([text_city for text_city in text_cities if
                                             self.clean_city(text_city).startswith(locations[1]) or self.clean_city(
                                                 text_city).startswith(locations[1].replace(" ", "-"))])
                    else:
                        origins.extend([text_city for text_city in text_cities if
                                        text_city.startswith(locations[1]) or text_city.startswith(
                                            locations[1].replace(" ", "-"))])
                        destinations.extend([text_city for text_city in text_cities if
                                             self.clean_city(text_city).startswith(locations[0]) or self.clean_city(
                                                 text_city).startswith(locations[0].replace(" ", "-"))])

        if not origins and not destinations and len(locations) == 2:
            origins.extend([text_city for text_city in text_cities if
                            text_city.startswith(locations[0]) or text_city.startswith(locations[0].replace(" ", "-"))])
            destinations.extend([text_city for text_city in text_cities if
                                 self.clean_city(text_city).startswith(locations[1]) or self.clean_city(
                                     text_city).startswith(
                                     locations[1].replace(" ", "-"))])

        if len(locations) == 2:
            if locations[0] in origins:
                origins = difflib.get_close_matches(locations[0], origins)
            if locations[0] in destinations:
                destinations = difflib.get_close_matches(locations[0], destinations)
            if locations[1] in origins:
                origins = difflib.get_close_matches(locations[1], origins)
            if locations[1] in destinations:
                destinations = difflib.get_close_matches(locations[1], destinations)

        if not origins and destinations:
            for location in locations:
                if len(difflib.get_close_matches(location, destinations)) == 0:
                    origins.extend([text_city for text_city in text_cities if
                                    self.clean_city(text_city).startswith(location) or self.clean_city(
                                        text_city).startswith(
                                        location.replace(" ", "-"))])
            if not origins:
                for location in locations:
                    if len(difflib.get_close_matches(location, destinations)) == 0 and len(location.split(" ")) > 1:
                        for loc_split in location.split(" "):
                            if loc_split not in prefix_words:
                                origins.extend([text_city for text_city in text_cities if
                                                self.clean_city(text_city).startswith(loc_split) or self.clean_city(
                                                    text_city).startswith(loc_split.replace(" ", "-"))])
        if origins and not destinations:
            for location in locations:
                if len(difflib.get_close_matches(location, origins)) == 0:
                    destinations.extend([text_city for text_city in text_cities if
                                         self.clean_city(text_city).startswith(location) or self.clean_city(
                                             text_city).startswith(
                                             location.replace(" ", "-"))])
            if not destinations:
                for location in locations:
                    if len(difflib.get_close_matches(location, origins)) == 0 and len(location.split(" ")) > 1:
                        for loc_split in location.split(" "):
                            if loc_split not in prefix_words:
                                destinations.extend([text_city for text_city in text_cities if
                                                     self.clean_city(text_city).startswith(
                                                         loc_split) or self.clean_city(
                                                         text_city).startswith(loc_split.replace(" ", "-"))])
        if len(origins) > 1:
            temp_origins = []
            for t in text_split:
                if t not in wrong_prefix_words and t.lower() != "gare" and any(t.lower() in o for o in origins):
                    if not temp_origins:
                        temp_origins.extend([origin for origin in origins if t.lower() in origin])
                    else:
                        temp_origins = list(
                            set(temp_origins).intersection([origin for origin in origins if t.lower() in origin]))
            origins = temp_origins
        if len(destinations) > 1:
            temp_destinations = []
            for t in text_split:
                if t not in wrong_prefix_words and t.lower() != "gare" and any(t.lower() in d for d in destinations):
                    if not temp_destinations:
                        temp_destinations.extend(
                            [destination for destination in destinations if t.lower() in destination])
                    else:
                        temp_destinations = list(set(temp_destinations).intersection(
                            [destination for destination in destinations if t.lower() in destination]))
            destinations = temp_destinations

        if not origins or not destinations:
            raise HTTPException(status_code=403, detail="Please ask a travel order between two cities")

        return {
            "origins": list(dict.fromkeys(origins)),
            "destinations": list(dict.fromkeys(destinations))
        }
