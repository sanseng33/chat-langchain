from flask import Flask, request, render_template, jsonify

from graph.intent import textFix

app = Flask(__name__)  # Flask APP


@app.route('/info', methods=['POST'])
def info():
    request_data = request.get_json()
    response_data = textFix(request_data['question'])
    return jsonify(response_data)


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)