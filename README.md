A deep learning model which answers frequently asked questions on BITSAT (Bits Pilani entrance exams)

#HOW TO RUN

1. Make a virtual  environment named "faqmodel" and install all packages from requirments.txt in 'FAQ-Retrieval' folder, using following command -> pip install -r requirements.txt

2. Make a ANOTHER virtual  environment named "qnaranking" and install all packages from requirments.txt in 'Ranking-Based-Question-Answering-System' folder, using following command -> pip install -r requirements.txt

3. Open terminal and activate "faqmodel" environment. Go to 'FAQ-Retrieval/src/' and run the command -> python driver.py

4. A flask server for API calls is up on localhost:5001

5. Open new terminal with new profile and activate "qnaranking" environment. Go to 'Ranking-Based-Question-Answering-System/Code/WebService/' and run the command -> python app.py

6. A flask server for API calls is up on localhost:5000

7. Now open 'index.html' in 'UI' folder on a browser (Chrome preferred) and type a search query and click on search button. 