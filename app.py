from flask import Flask, render_template, request, redirect, session
import copy
import time
from storygeneration.combined import generateStory
from threading import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session encryption

def promptProcess():
    global prompts, session_ids
    while True:
        unsolved_prompts = [{key:prompts[key]["prompt"]} for key in prompts.keys() if prompts[key]["result"] == None and prompts[key]["prompt"] != None]
        if len(unsolved_prompts) > 0:
            current_prompt = unsolved_prompts[0]
            currentId = list(current_prompt.keys())[0]
            text = generateStory("Default", current_prompt[currentId])
            prompts[currentId]["result"] = text
        else:
            time.sleep(0.2)

@app.route('/home', methods=['GET', 'POST'])
def home():
    global prompts, session_ids
    print(session.keys())
    if "sessionId" not in session.keys() or session["sessionId"] not in prompts.keys():
        session_ids += 1
        session["sessionId"] = copy.deepcopy(session_ids)
        prompts[session["sessionId"]] = {}
        prompts[session["sessionId"]]["prompt"] = None
        prompts[session["sessionId"]]["result"] = None
        
    if request.method == 'POST':
        prompt = request.form.get("promptInput")
        prompts[session["sessionId"]]["prompt"] = prompt
        prompts[session["sessionId"]]["result"] = None
        while prompts[session["sessionId"]]["result"] == None:
            time.sleep(0.2)
    if prompts[session["sessionId"]]["result"] != None:
        result = prompts[session["sessionId"]]["result"]
    else:
        result = ""
    return render_template('index.html', result=result)

@app.route('/result')
def result():
    prompt = session.get('prompt')  # Retrieve the prompt from the session
    if prompt:
        result = generateStory(prompt)  # Call your function to generate the story
        session.pop('prompt')  # Remove the prompt from the session after processing
        return render_template('index.html', result=result)
    return "No prompts available."

@app.route('/about')
def about():
    return render_template('team.html')

@app.route('/stories')
def stories():
    return render_template('stories.html')


if __name__ == '__main__':
    global prompts, session_ids
    prompts = {}
    session_ids = 0
    T = Thread(target=promptProcess, daemon=True)
    T.start()
    app.run()