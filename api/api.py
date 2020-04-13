from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from simpletransformers.question_answering import QuestionAnsweringModel
from googlesearch import search
from documentretriever import DocumentRetriever
import pandas as pd
from qamodelloader import QAModelLoader

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



documentRetriever = DocumentRetriever(data_path = "./data/bnpp_newsroom-v1.1.csv")
model = QAModelLoader()

# model_path = 'D:/Deep_learning/Workspace/Question_Answering_System/model/best_model_2/'
# model = QuestionAnsweringModel('bert', model_path, use_cuda=False)

@app.route('/fromcollecteddata', methods=['GET'])
def fromcollecteddata():

    query = 'Since when does the Excellence Program of BNP Paribas exist?'
    squad_examples = documentRetriever.get_most_relevant_paragraph(query)
    context = squad_examples['paragraphs'][0]['context']
    answer = model.answer(query, context)
    print(answer)

    return jsonify({
        'query': query, 
        'answer': answer,
        'paragraph': context
    })


@app.route('/fromgooglesearch', methods=['GET'])
def fromgooglesearch():

    query = request.args.get("query")
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
