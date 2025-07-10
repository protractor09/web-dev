import flask
from flask import request, jsonify
from flask_cors import CORS
from llm import get_res,gen_cover_letter
import requests

app=flask.Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/gen',methods=['POST'])
def gen():
    try:
        data=request.get_json()
        resume = data.get('resume')
        jd=data.get('jd')

        if not resume or not jd:
            return jsonify({"error": "Resume and job description are required"}), 400

        result=get_res(resume, jd)
        return result
    except Exception as e:
        return jsonify({"error":str(e)}),500
    

@app.route('/cover_letter',methods=['GET','POST'])
def gen_cover():
    try:
        data=request.get_json()
        resume = data.get('resume')
        jd=data.get('jd')

        if not resume or not jd:
            return jsonify({"error": "Resume and job description are required"}), 400

        result=gen_cover_letter(resume, jd,'abc')
        return jsonify({"cover_letter": result})
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
if __name__=='__main__':
    app.run(debug=True)