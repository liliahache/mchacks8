
# Imports the Google Cloud client library
from google.cloud import storage

from natlangclasscloud import sample_classify_text
from get_topics import recommendation

import random

def remove_punctuation(user_input):
    lower_input = user_input.lower()

    # define punctuation
    punctuations = '''!()-[]\{\};:'"\,<>./?@#$%^&*_~'''

    # remove punctuation from the string
    no_punct = ""
    for char in lower_input:
        if char not in punctuations:
            no_punct = no_punct + char

    return no_punct

def get_diy_answers(user_input):
    
    no_punct = remove_punctuation(user_input)

    if no_punct in ["hi", "hello", "hey", "hola", "bonjour", "allo", "salut"]:

        # if we couldn't find any in the same category:
        greetings = ["Hello! Please tell me what you like so I can recommend some books!\n",
                    "Hi. I can recommend so many good books!\n",
                    "It's nice to meet you! I hope I can inspire you to read a new book today.\n",
                    "Hello there. Tell me what you're into and I will give you books to read.\n"]
        return random.choice(greetings)
    
    if no_punct in ["how are you", "whats up", "how are you going", "hows your day been", "how do you do", "comment ça va", "comment ca va", "ca va", "hows it going"]:
        how_are_you = ["I'm good! Let me help you find a book to read.\n",
                    "Fine, thank you. Ready to recommend some books to read!\n",
                    "I'm great! Please let me know what kind of books you like.\n",
                    "Doing good... Tell me what you like to read about please!\n"]
        return random.choice(how_are_you)

    if no_punct in ["what do you do", "help me", "how can you help", "how can you help me", "how do you work", "comment fonctionnetu", "what is going on"]:
        what_you_do = ["Tell me about your hobbies and interests, and I will tell you what books you would like.\n",
                    "I help people like you find books to read, based on their interests!\n",
                    "I am a slave of the Google Cloud... I have to recommend books all day!\n",
                    "Please tell me about yourself, and I will give you book recommendations.\n"]
        return random.choice(what_you_do)

    if no_punct in ["whats your name", "who are you", "qui est tu", "quel est ton nom"]:
        name = ["I am Alexandria! I recommend the best books for your unique taste.\n",
                    "My name is Alexandria and I love books. Please let me help you find one to read!\n",
                    "Alexandria. I recommend books!\n",
                    "Alexandria from the Library of Alexandria! I'm famous for recommended the best books.\n"]
        return random.choice(name)

    return None


def get_book_rec(user_input):

    # check if user input is one of our own categories
    diy_rec = get_diy_answers(user_input)

    if diy_rec:
         return diy_rec


    # get a minimum of twenty words
    twenty_stop_words = " the" * 20
    long_user_input = user_input + twenty_stop_words

    # overwrite input1.txt -> write the user string input
    with open("input1.txt", "w", encoding='utf-8') as f:
        f.write(long_user_input)

    # send user input to input1.txt in the google cloud
    bucket_name = "trismegistus_ballsac"
    source_file_name = "input1.txt"
    destination_blob_name = "input1.txt"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    category = sample_classify_text('gs://trismegistus_ballsac/input1.txt')

    book_rec = recommendation(category)
    
    return book_rec
    
# start of Jere Xu's code, from his github: https://github.com/jerrytigerxu/Simple-Python-Chatbot"
# jerrytigerxu's code was used a a template, and we modified the look of it slightly

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        res = get_book_rec(msg)
        ChatLog.insert(END, "Alexandria: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

#Creating GUI with tkinter
import tkinter
from tkinter import *

base = Tk()
base.title("Library of Alexandria")
base.geometry("800x500")
base.resizable(width=FALSE, height=FALSE)


#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="4", width="30", font=("Arial",16, 'bold'))
ChatLog.config(state=DISABLED)


#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set


#Create Button to send message
SendButton = Button(base, font=("Arial",16, 'bold'), text="Send", width="12", height=3,
                    bd=0, bg="#3d998a", activebackground="#90ee90",activeforeground="#3d998a",
                    fg='#90ee90', command=send )


#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="20", height="2", font=("Arial",16, 'bold'))


#Place all components on the screen
scrollbar.place(x=776,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=770)
EntryBox.place(x=128, y=401, height=90, width=665)
SendButton.place(x=6, y=401, height=90)


base.mainloop()

# end of Jere Xu's code