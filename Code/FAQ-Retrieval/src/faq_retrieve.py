import preprocessing as preprocess
from sentence_transformers import SentenceTransformer
import numpy as np

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

# loading SBERT model
def load_model():
	sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
	return sbert_model

# get SBERT embeddings
def get_sbert_embeddings(model, sentences):
    return model.encode(sentences)

def encode_faq(model,processed_QA_df, isfaq=False):
    sentences = processed_QA_df
    if isfaq :
        sentences = processed_QA_df["questions"].to_list()
    question_QA_sbert_embeddings = get_sbert_embeddings(model,sentences)
    return question_QA_sbert_embeddings

def evaluate_sbert(question_sbert_embeddings, query_sbert_embeddings, train_QA_df, train_column_name, test_QA_df, test_column_name):

    query = ""
    retrieved_ques = ""
    answer = ""

    for test_index, test_vector in enumerate(query_sbert_embeddings):
        sim, sim_Q_index, sim2, sim_Q_index2 = -1, -1, -1, -1
        for train_index, train_vector in enumerate(question_sbert_embeddings):
            sim_score = cosine(train_vector, test_vector)
            
            if sim < sim_score:
                sim2 = sim
                sim_Q_index2 = sim_Q_index
                sim = sim_score
                sim_Q_index = train_index

            elif sim2 < sim_score:
              sim2 = sim_score
              sim_Q_index2 = train_index
              
        query = test_QA_df[test_column_name].iloc[test_index]
        
        retrieved_ques = train_QA_df[train_column_name].iloc[sim_Q_index]
        if sim >= 0.5:   #threshold value
            answer = train_QA_df["answers"].iloc[sim_Q_index]
            
        # to print query and corresponding retrieved question
        print("######")
        print(f"Query Question: {query}")    
        print(f"Retrieved Question 1: {retrieved_ques}")
        print(f"Retrieved Answer : {answer}")
        # print(f"Retrieved Question 2: {train_QA_df[train_column_name].iloc[sim_Q_index2]}")
        print("######")
        
    if answer == '':
        final_ans = {
            "faq" : "No results from FAQ database", "retrieved_question": 'NONE', "retrieved_answer": 'NONE'}
    else:
        final_ans = {"faq" : "Results from FAQ database", "retrieved_question": retrieved_ques, "retrieved_answer": answer}

    return final_ans

def evaluate(question_sbert_embeddings, query_sbert_embeddings, processed_faq, processed_query):
    return evaluate_sbert(question_sbert_embeddings, query_sbert_embeddings, processed_faq, "questions", processed_query, "questions")
    


