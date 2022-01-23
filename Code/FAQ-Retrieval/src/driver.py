import preprocessing as preprocess
import faq_retrieve as faqr
import pandas as pd
import json

from flask import Flask, request, Response, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello():
   return 'Server Up and Running!'

@app.route('/faqanswer', methods = ["GET","POST"])
def callFaqModel():
   
	question = str(request.form["question"])
	#########call faq models and return json format##########
	faq_dataset = preprocess.load_file()

	# pre-process training question data
	text_preprocessor = preprocess.TextPreprocessor(faq_dataset.copy(), column_name="questions")
	processed_faq_dataset = text_preprocessor.process(perform_stopword=True)

	model = faqr.load_model()
	encoded_faq = faqr.encode_faq(model, processed_faq_dataset,True)

	test_query_string = [question]
						# ["How to know if I am eligible to apply for BITSAT?"]
	                    # "Can I get the application form via mail?",
	                    #"What are the fees?",
	                    #"Can I appear for BITSAT 2020 if I also took BITSAT 2019?",
	                    #"Can I appear if I failed 12th"]

	test_query_df = pd.DataFrame(test_query_string, columns=["questions"]) 

	# pre-process test query data
	text_preprocessor = preprocess.TextPreprocessor(test_query_df, column_name="questions")
	processed_query = text_preprocessor.process(perform_stopword=True)

	encoded_query = faqr.encode_faq(model, test_query_string,False)

	# final answer can be retrieved question/null based on confidence value
	faqResult = faqr.evaluate(encoded_faq, encoded_query, processed_faq_dataset, processed_query)

	# make json response
	response = jsonify(faqResult)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


if __name__ == '__main__':
   app.run(host = '127.0.0.1', port = 5001, debug = True)
