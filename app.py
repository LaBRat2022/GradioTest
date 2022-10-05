import numpy as np
import gradio as gr
import random
import string
import soundfile as sf
#from random_word import RandomWords
import requests
#import bot as bot



# All this to import Whisper # from stackoverflow
import collections.abc
#hyper needs the four following aliases to be done manually.
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping

# Text Generator Macine #
import whisper


# API Work #

key = "Your Speechace Key here"
api_endpoint = "https://api.speechace.co" 
url = api_endpoint + "/api/scoring/text/v0.5/json"
dialect = "en-us"
user_id = "81ozow"

url += '?' + 'key=' + key + '&dialect=' + dialect + '&user_id=' + user_id 

def grade(target, audio):

    #text Work#
    text = str(random.randint(0, 100))

    payload = {'text':target}
    print(payload)

    #Audio work#
    sr, data = audio
    sf.write('temp.wav', data, 44100)
    user_file_handle = open('temp.wav', 'rb')
    files = {'user_audio_file': user_file_handle}

    response = requests.post(url, data=payload, files=files)
    totalscore = response.json() #respuesta a json thing
    
    return 'Target practice: ', target, ' Your score is: ', totalscore['text_score']['quality_score']


def whispertranscribe(model, audio):

    # Audio Work #
    sr, data = audio
    sf.write('temp.wav', data, 44100)
    audiofile = open('temp.wav', 'rb')

    # Model work and send to Whisper #
    model = whisper.load_model(model)
    result = model.transcribe('temp.wav')
    #jresult = result.json()

    return result['text']


def generate(range):

    rvalue = random.randint(0,range)

    return rvalue


def genletter(numberofletters):

    letters = string.ascii_lowercase
    rletter = random.choices(letters, k=int(numberofletters))

    return rletter


def genword(numberofletters):

    #rword = RandomWords()
    #3rword = rword.get_random_word()

    return #rword


##############################################  APP BEGINS HERE ##################################################################



englishcoach = gr.Blocks()

with englishcoach:

    gr.Markdown("Hello! This is the English basic pronunciation Coach")
    with gr.Tabs():
        
        with gr.TabItem("Alphabet"):

            with gr.Row():

                with gr.Column():
                    numberofletters = gr.Number(value=1, label='Letters to practice:')
                    gen_button = gr.Button("Generate")
                
                randomletter = gr.Textbox(label="Target Letter: ")
                gen_button.click(fn=genletter, inputs=numberofletters, outputs=randomletter)
            
            gr.Markdown("Click the box below to test your pronunciation!")
            audio = gr.Audio(source='microphone')
            rec_button = gr.Button("Test your Pronunciation! ")
                
            gradebox = gr.Textbox(label='Your score: ')
            rec_button.click(fn=grade, inputs=[randomletter, audio], outputs=gradebox)


        with gr.TabItem("Word Practice"):

            with gr.Column():
                gen_button = gr.Button("Generate")
                numberofletters = gr.Textbox(label="Target Word: ")
                gen_button.click(fn=genword, inputs=numberofletters, outputs=numberofletters)

         
            audio = gr.Audio(source='microphone')
            rec_button = gr.Button("Test your Pronunciation! ")
            gradebox = gr.Textbox(label='Your score: ')
            rec_button.click(fn=grade, inputs=[numberofletters, audio], outputs=gradebox)


        with gr.TabItem("Numbers"):

            with gr.Row():
                range = gr.Radio([10, 100, 1000], label="Practice numbers between 0 and ...")
                randomnumber = gr.Textbox(label="Target Number: ")
            
            with gr.Row():
                gen_button = gr.Button("Generate")
                gen_button.click(fn=generate, inputs=range, outputs=randomnumber)

            audio = gr.Audio(source='microphone')
            rec_button = gr.Button("Test your Pronunciation! ")
            gradebox = gr.Textbox(label='Your score: ')
            rec_button.click(fn=grade, inputs=[randomnumber, audio], outputs=gradebox)

        with gr.TabItem("Whisper"):

            with gr.Row():
                model = gr.Radio(['tiny', 'base', 'small'],value='tiny', label="Pick the Whisper size: ")
                #randomnumber = gr.Dropdown(label="Spoken Language: ")

            audio = gr.Audio(source='microphone')
            rec_button = gr.Button("Click to Transcribe! ")
            transbox = gr.Textbox(label='Your transcription: ')
            rec_button.click(fn=whispertranscribe, inputs=[model, audio], outputs=transbox)



englishcoach.launch()