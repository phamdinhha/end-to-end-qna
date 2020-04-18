from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from simpletransformers.question_answering import QuestionAnsweringModel
from googlesearch import search
from documentretriever import DocumentRetriever
import pandas as pd
from qamodelloader import QAModelLoader
from customdocumentretriever.customgooglesearchengine import CustomGoogleSearchEngine

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


model = QAModelLoader()
data_path = "./data/customdata.csv"

@app.route('/fromgoolesearch', methods=['GET'])
def fromgooglesearch():

    query = request.args.get("query")
    search_engine = CustomGoogleSearchEngine(query)
    doc_trunk = search_engine.buildDocumentTrunk()
    documentRetriever = DocumentRetriever(data_path = doc_trunk)
    squad_examples = documentRetriever.get_most_relevant_paragraph(query)
    context = squad_examples['paragraphs'][0]['context']
    print(context)
    answer = model.answer(query, context)
    #print(paragraphs[0])
    print(answer)
    return jsonify({
        'query': query, 
        'answer': answer,
        'paragraph': context
    })


@app.route('/fromcustomdata', methods=['GET'])
def fromcollecteddata():

    query = request.args.get("query")
    documentRetriever = DocumentRetriever(data_path = data_path)
    squad_examples = documentRetriever.get_most_relevant_paragraph(query)
    context = squad_examples['paragraphs'][0]['context']
    answer = model.answer(query, context)
    print(answer)

    return jsonify({
        'query': query, 
        'answer': answer,
        'paragraph': context
    })

if __name__ == '__main__':
    app.run()
