import tkinter
from tkinter import *
import string
import re
import pyttsx3
import random
import warnings
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import numpy as np


def app():

    warnings.filterwarnings('ignore')
    #Packages for nltk
    nltk.download('punkt',quiet=True)
    nltk.download('wordnet',quiet=True)


    def botResponse(user_query):


        user_response = user_query
        #Getting Contents/Articles
        url = 'article.html'
        page = open(url)
        soup = BeautifulSoup(page.read())
        corpus = soup.get_text()



        #Tokenization
        text=corpus
        tokens = nltk.sent_tokenize(text)


        #Punctuation removal
        remove_punctuation = dict( (ord(punct),None) for punct in string.punctuation)

        #Lemmatization and Normalization
        def LemmaNormalize(text):
            lemmas = nltk.word_tokenize(text.lower().translate(remove_punctuation))
            return lemmas


        #Small Talks
        Greeting_inputs =["hi", "hello", "namaskar", "heya", "hii", "helo", "hey", "hiii"]
        Greeting_response = ["hi Pillaite","hello there","heya","hi","Hi there","Howdy","How can i help?","Hey","Nice to see you"]

        #Small Talk generator
        def Greetings(sentence):
            for word in sentence.split():
                if word.lower() in Greeting_inputs:
                    return random.choice(Greeting_response)


        #Bot Response for queries
        #Speech 
        def Speak(response):
            engine = pyttsx3.init()
            engine.say(response)
            engine.runAndWait()
            
        def Response(user_response):
            response = ''
            tokens.append(user_response)
            Tfidfvector = TfidfVectorizer(tokenizer= LemmaNormalize, stop_words='english')
            tfidf = Tfidfvector.fit_transform(tokens)

            #Similarity Finder
            similarity = cosine_similarity(tfidf[-1],tfidf)
            index = similarity.argsort()[0][-2]
            flat = similarity.flatten()
            flat.sort()
            sim_score = flat[-2]

            if(sim_score == 0):
                response = response + "Didn't Get You, Sorry"

            else:
                response = response + tokens[index]

            tokens.remove(user_response)
            return  response


        flag = True

        while(flag==True):
                user_response = user_query
                user_response = user_response.lower()
                if(user_response!='bye'):
                    if(user_response=='thanks' or user_response=='thank you' or user_response=='quit'):
                        flag = False
                        response = 'Welcome'
                        return response
                    else:
                        if(Greetings(user_response)!=None):
                            response = Greetings(user_response)
                            return response
                        else:
                            response = Response(user_response)
                            return response
                else:
                    flag = False
                    response = 'Bye'
                    return response




    #GUI Builder
    def send():
        msg = EntryBox.get("1.0",'end-1c').strip()
        EntryBox.delete("0.0",END)
        if msg != '':
            if msg=='bye' or msg=='quit':
                Chatlog.config(state=NORMAL)
                Chatlog.insert(END, "You: " + msg + '\n\n')
                Chatlog.config(foreground="white", font=("Verdana", 12))
                res = botResponse(msg)
                Chatlog.insert(END, "Bot: " + res + '\n\n')
                Chatlog.config(state=DISABLED)
                Speak(response)

                base.after(1000, lambda: base.destroy())


            else:
                Chatlog.config(state=NORMAL)
                Chatlog.insert(END, "You: " + msg + '\n\n')
                Chatlog.config(foreground="white", font=("Verdana", 12))
                res = botResponse(msg)
                Chatlog.insert(END, "Bot: " + res + '\n\n')
                Chatlog.config(state=DISABLED)
                Speak(response)






    base = Tk()
    base.title('ClassBot')
    base.geometry("400x500")
    base.resizable(width=False,height=False)

    Chatlog = Text(base, bd=0, bg="#17202A ", height="8", width="50", font="Arial",)
    Chatlog.config(state=DISABLED)


    scrollbar = Scrollbar(base, command=Chatlog.yview, cursor="heart")
    Chatlog['yscrollcommand'] = scrollbar.set


    SendButton = Button(base, font=("Verdana",12,'bold'), text="Englsih", width="6", height=5,
                        bd=0, bg="#27AE60 ", activebackground="#82E0AA ",fg='#ffffff',
                        command= send )





    EntryBox = Text(base, bd=0, bg="#FDEDEC",width="28", height="5", font="Arial")



    #Place all components on the screen
    scrollbar.place(x=376,y=6, height=386)
    Chatlog.place(x=6,y=6, height=386, width=370)
    EntryBox.place(x=128, y=401, height=90, width=265)
    SendButton.place(x=10, y=450, height=30)
    base.mainloop()


if __name__ == "__main__":
    app()
