from pathlib import Path
import os, re, io
import pandas as pd
import numpy as np
import requests

## stopwords
from gensim.parsing.preprocessing import remove_stopwords
## lemma functionality provide by NLTK
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')
from nltk import word_tokenize
#nltk.download('punkt')
import spacy
nlp = spacy.load('en')

from gensim.models import TfidfModel
from gensim.corpora import Dictionary
## cosine similarity
from sklearn.metrics.pairwise import cosine_similarity

path = Path("../data/")
in_path = str(path / "BITSAT-FAQ.csv")

def load_file():
	QA_df = pd.read_csv(os.path.join(in_path),header=None)
	QA_df.columns = ['questions','answers']
	# QA_df = QA_df[:15]
	return QA_df

# Data Preprocessing
class TextPreprocessor():
    def __init__(self, data_df, column_name=None):
        self.data_df = data_df  
        if not column_name and type(colum_name) == str:
            raise Exception("column name is mandatory. Make sure type is string format")
        self.column = column_name
        self.convert_lowercase()    
        self.applied_stopword = False
        self.processed_column_name = f"processed_{self.column}"
        
    def convert_lowercase(self):
        ## fill empty values into empty
        self.data_df.fillna('',inplace=True)
        ## reduce all the columns to lowercase
        self.data_df = self.data_df.apply(lambda column: column.astype(str).str.lower(), axis=0)    

    def remove_question_no(self):
        ## remove question no        
        self.data_df[self.column] = self.data_df[self.column].apply(lambda row: re.sub(r'^\d+[.]',' ', row))    
        
    def remove_symbols(self):
        ## remove unwanted character          
        self.data_df[self.column] = self.data_df[self.column].apply(lambda row: re.sub(r'[^A-Za-z0-9\s]', ' ', row))    

    def remove_stopwords(self):
        ## remove stopwords and create a new column 
        for idx, question in enumerate(self.data_df[self.column]):      
            self.data_df.loc[idx, self.processed_column_name] = remove_stopwords(question)        

    def apply_lemmatization(self, perform_stopword):
        ## get the root words to reduce inflection of words 
        lemmatizer = WordNetLemmatizer()    
        ## get the column name to perform lemma operation whether stopwords removed text or not
        if perform_stopword:
            column_name = self.processed_column_name
        else:
            column_name = self.column
        ## iterate every question, perform tokenize and lemma
        for idx, question in enumerate(self.data_df[column_name]):

            lemmatized_sentence = []
            ## use spacy for lemmatization
            doc = nlp(question.strip())
            for word in doc:       
                lemmatized_sentence.append(word.lemma_)      
                ## update to the same column
                self.data_df.loc[idx, self.processed_column_name] = " ".join(lemmatized_sentence)

    def process(self, perform_stopword = True):
        self.remove_question_no()
        self.remove_symbols()
        if perform_stopword:
            self.remove_stopwords()
        self.apply_lemmatization(perform_stopword)    
        return self.data_df




