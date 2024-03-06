from flask import Flask, request, render_template, jsonify

from aider.parse import codeParse

app = Flask(__name__)  # Flask APP


@app.route('/code', methods=['POST'])
def code():
    request_data = request.get_json()
    response_data = codeParse(request_data['question'])
    print(response_data)
    return response_data


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)