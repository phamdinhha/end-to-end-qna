# End to end QNA

This is a simple end to end question answering system that was built to get some practical experiences with BERT.

## Model
BERT (Bidirectional Encoder Representations from Transformers) is a recent model published by researchers at Google AI Language. It has caused a stir in the Machine Learning community by presenting state-of-the-art results in a wide variety of NLP tasks, including Question Answering (SQuAD v1.1), Natural Language Inference (MNLI), and others.

In this example I choose BERT-multililgual-cased. The model was fine-tunned for Question and Answer task with the SQUAD 2.0 data set.
All the fine-tunning process was done on google colab, so no heavy-duty server was required to try on BERT, but of course, I only can fine-tune a basic model and the valuation score was not good.
## Api
The api was written by Python3:

- Takes a question as the query input
- Use the question to retrive the most related paragraph from document trunks
- The first api takes the question and perform google search and then generate the document trunk
- The second api takes an existing document trunk as the input
- The question and paragraphs are then passed to BERT model to generate the answer
## UI
The web ui was written based on VueJs and I'm still updating this.
## References
## Demo
![demo](/demo/demo2.png)
