from flask import Flask, render_template, jsonify, request
import requests

app=Flask(__name__)

@app.route('/')
def indeex():
    return  render_template('index.html')


@app.route('/chat',methods=['POST'])
def chat():
    user_msg=request.form.get('message')

    try:
        response= requests.post("http://localhost:11434/api/generate", json={
            "model":"mistral",
            "prompt":user_msg,
            "stream":False
        })
        response.raise_for_status()
        bot_reply=response.json().get("response","no reply")
    except Exception as e:
        bot_reply=e
        print(bot_reply)
    return jsonify({'response':bot_reply})

if __name__=='__main__':
    app.run(debug=True)