from flask import Flask, request, render_template, jsonify

from aider.commit import commit_all
from aider.parse import codeParse
from flask_cors import CORS

app = Flask(__name__)  # Flask APP
CORS(app)

PROJECT_ID = '7193'  # 您的项目ID

@app.route('/code', methods=['POST'])
def code():
    request_data = request.get_json()
    response_data = codeParse(request_data['question'], request_data['continuation_data'])
    print(response_data)
    return response_data

@app.route('/commits', methods=['GET'])
def commits():
    response_data = commit_all(PROJECT_ID)
    return response_data


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)