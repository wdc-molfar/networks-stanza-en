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
from network import directed_weighted_network_terms
from netprocessing import network_json
from netprocessing import json_to_network, network_to_matrix
from dissimilarity import frobenius
import os, io

warnings.filterwarnings("ignore", message=r"\[W033\]", category=UserWarning)


# Load stop words
def load_stop_words(lang):
    if os.path.isfile(lang + '.txt'):
        stop_words = (io.open(lang + '.txt', 'r', encoding="utf-8").read()).split()
    else:
        stop_words = []
    return stop_words


# Formation semantic network
def semantic_network(text, model, stop_words):
    allTermsTags, sentsTermsTags = stanza_nlp(text, model, stop_words)
    allTermsTagsGTF = tuples_builder(allTermsTags)
    sentsTseries, sentsTuples = time_series(allTermsTagsGTF, sentsTermsTags)

    dwnt = directed_weighted_network_terms(sentsTuples)
    return {"network_json": network_json(dwnt)}


# Calculate semantic dissimilarity.py of two networks
def semantic_similarity(json_network1, json_network2):
    # Convert JSON to networkx
    network1 = json_to_network(json_network1)
    network2 = json_to_network(json_network2)

    # Get all unique nodes from two networks
    nodelist = list(set(list(network1.nodes()) + list(network2.nodes())))

    # Add all the nodes from one network to another
    network1.add_nodes_from(network2)
    network2.add_nodes_from(network1)

    # Return the graph adjacency matrix as a NumPy matrix
    matrix1 = network_to_matrix(network1, nodelist)
    matrix2 = network_to_matrix(network2, nodelist)

    return {"dissimilarity": frobenius(matrix1, matrix2)}

# Create subclasses defining the schema, or data shapes, you want to receive for run_semantic_network
class Item_network(BaseModel):
    text: str

    class Config:
        orm_mode = True


# Create subclasses defining the schema, or data shapes, you want to receive for run_semantic_similarity
class Item_similarity(BaseModel):
    network1: str
    network2: str

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
@app.post("/network")
# Define the path operation function
async def run_semantic_network(input_json: Item_network):
    # Get text from input JSON object
    text = input_json.text

    try:
        output = {"request": input_json, "response": semantic_network(text, model, stop_words)}

    except BaseException as ex:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        output = {"error": ''}
        output['error'] += "Exception type : %s; \n" % ex_type.__name__
        output['error'] += "Exception message : %s\n" % ex_value
        output['error'] += "Exception traceback : %s\n" % "".join(
            traceback.TracebackException.from_exception(ex).format())

    return output

# Define a path POST-operation decorator
@app.post("/similarity")
# Define the path operation function
async def run_semantic_similarity(input_json: Item_similarity):
    # Get text from input JSON object
    json_network1 = input_json.network1
    json_network2 = input_json.network2

    try:
        output = {"request": input_json, "response": semantic_similarity(json_network1, json_network2)}

    except BaseException as ex:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        output = {"error": ''}
        output['error'] += "Exception type : %s; \n" % ex_type.__name__
        output['error'] += "Exception message : %s\n" % ex_value
        output['error'] += "Exception traceback : %s\n" % "".join(
            traceback.TracebackException.from_exception(ex).format())

    return output