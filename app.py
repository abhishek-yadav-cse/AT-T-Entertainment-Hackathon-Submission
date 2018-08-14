from flask import Flask, request, render_template, url_for, jsonify
from bs4 import BeautifulSoup
from newspaper import Article
from nltk.tokenize import sent_tokenize
import requests
from swn_simple import *


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result',methods=['POST','GET'])
def cal():
    if request.method=='POST':
        result=request.form['headline']
        data = [result]
        entered_sentence = data
    
        #url = 'http://www.foxnews.com/us/2018/07/27/two-massachusetts-police-officers-shot-while-investigating-disturbance-authorities-say.html'
        a = Article(result)

        a.download()
        a.parse()

        #mystring = a.text.replace('\n', ' ')
        mystring = a.title.replace('\n', ' ')

        sent_tokenize_list = sent_tokenize(mystring)
        #for (var i=0; i<sent_tokenize_list.length; i++) {
#Sheen
        sheen_string = [process_sentence(x) for x in sent_tokenize_list]
    #print(sent_tokenize_list)
    return render_template('happy.html',mystring=mystring, entered_sentence=entered_sentence, sheen_string='. '.join(sheen_string))


if __name__ == '__main__':
    app.debug = True
     
    # print(scrape())
    app.run(host='0.0.0.0')