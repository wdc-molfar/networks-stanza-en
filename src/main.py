# main.py

# Import FastAPI
from fastapi import FastAPI
# Import BaseModel from pydantic
from pydantic import BaseModel
import stanza
import sys
import traceback
import warnings
from models import download_model, load_model
from nlprocessing import stanza_nlp
from weighers import tuples_builder, time_series
from networks import directed_weighted_network_terms
from graphprocessing import network_json
import os, io

warnings.filterwarnings("ignore", message=r"\[W033\]", category=UserWarning)


def load_stop_words(lang):
    if os.path.isfile(lang + '.txt'):
        stop_words = (io.open(lang + '.txt', 'r', encoding="utf-8").read()).split()
    else:
        stop_words = []
    return stop_words


def semantic_networks(text, model, stop_words):
    allTermsTags, sentsTermsTags = stanza_nlp(text, model, stop_words)
    allTermsTagsGTF = tuples_builder(allTermsTags)
    sentsTseries, sentsTuples = time_series(allTermsTagsGTF, sentsTermsTags)

    dwnt = directed_weighted_network_terms(sentsTuples)
    return {"network_json": network_json(dwnt)}


# Create subclasses defining the schema, or data shapes, you want to receive
class Item(BaseModel):
    text: str

    class Config:
        orm_mode = True


# Load EN stanza model
model = load_model("en")

# Load EN stop words
stop_words = load_stop_words("en")

# Create a FastAPI instance
app = FastAPI()


# Define a path GET-operation decorator
@app.get("/download")
async def download_stanza_model():
    download_model("en")
    return "Models loaded successfully!"


# Define a path POST-operation decorator
@app.post("/networks")
# Define the path operation function
async def run_semantic_networks(input_json: Item):
    # Get text from input JSON object
    text = input_json.text

    try:
        output = {"request": input_json, "response": semantic_networks(text, model, stop_words)}

    except BaseException as ex:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        output = {"error": ''}
        output['error'] += "Exception type : %s; \n" % ex_type.__name__
        output['error'] += "Exception message : %s\n" % ex_value
        output['error'] += "Exception traceback : %s\n" % "".join(
            traceback.TracebackException.from_exception(ex).format())

    return output
