import joblib
import warnings

import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator

from cdqadocumentretriever import TfidfRetriever, BM25Retriever
from utils.filters import filter_paragraphs 
from utils.converters import generate_squad_examples
from ast import literal_eval



RETRIEVERS = {"bm25": BM25Retriever, "tfidf": TfidfRetriever}


class DocumentRetriever(BaseEstimator):
    """
    A scikit-learn implementation of the whole cdQA pipeline

    Parameters
    ----------

    retriever: "bm25" or "tfidf"
        The type of retriever

    retrieve_by_doc: bool (default: True). If Retriever will rank by documents
        or by paragraphs.

    Examples
    --------
    >>> from documentretriever import DocumentRetriever
    >>> qa_pipeline = QAPipeline(reader='bert_qa_squad_vCPU-sklearn.joblib')
    >>> qa_pipeline.fit_retriever(X=df)
    >>> prediction = qa_pipeline.predict(X='When BNP Paribas was created?')

    >>> from cdqa.pipeline import QAPipeline
    >>> qa_pipeline = QAPipeline()
    >>> qa_pipeline.fit_reader('train-v1.1.json')
    >>> qa_pipeline.fit_retriever(X=df)
    >>> prediction = qa_pipeline.predict(X='When BNP Paribas was created?')

    """

    def __init__(self, data_path = "./data/bnpp_newsroom-v1.1.csv", retriever="bm25", retrieve_by_doc=False, **kwargs):

        if retriever not in RETRIEVERS:
            raise ValueError(
                "You provided a type of retriever that is not supported. "
                + "Please provide a retriver in the following list: "
                + str(list(RETRIEVERS.keys()))
            )

        retriever_class = RETRIEVERS[retriever]

        kwargs_retriever = {
            key: value
            for key, value in kwargs.items()
            if key in retriever_class.__init__.__code__.co_varnames
        }

        self.retriever = retriever_class(**kwargs_retriever)

        self.data_path = data_path

        self.retrieve_by_doc = retrieve_by_doc

    def fit_retriever(self):
        """ Fit the QAPipeline retriever to a list of documents in a dataframe.
        Parameters
        ----------
        df: pandas.Dataframe
            Dataframe with the following columns: "title", "paragraphs"
        """

        df = pd.read_csv( self.data_path,
                          converters={"paragraphs": literal_eval},
                        )

        df = filter_paragraphs(df)

        if self.retrieve_by_doc:
            self.metadata = df
            self.metadata["content"] = self.metadata["paragraphs"].apply(
                lambda x: " ".join(x)
            )
        else:
            self.metadata = self._expand_paragraphs(df)

        self.retriever.fit(self.metadata)

        return self

    def get_best_indexes(
        self,
        query: str = None
    ):
        best_idx_scores = self.retriever.predict(query)
        return best_idx_scores

    @staticmethod
    def _expand_paragraphs(df):
        # Snippet taken from: https://stackoverflow.com/a/48532692/11514226
        lst_col = "paragraphs"
        df = pd.DataFrame(
            {
                col: np.repeat(df[col].values, df[lst_col].str.len())
                for col in df.columns.drop(lst_col)
            }
        ).assign(**{lst_col: np.concatenate(df[lst_col].values)})[df.columns]
        df["content"] = df["paragraphs"]
        return df.drop("paragraphs", axis=1)

    def get_most_relevant_paragraph(self, query):
        self.fit_retriever()
        bestIndexes = self.get_best_indexes(query)
        squad_examples = generate_squad_examples(
            question=query,
            best_idx_scores=bestIndexes,
            metadata=self.metadata,
            retrieve_by_doc=self.retrieve_by_doc,
        )
        return squad_examples[0]

