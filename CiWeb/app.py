from flask import Flask, render_template, request

import maxMatch, generateCi

# app.debug = True
app = Flask(__name__)


@app.route('/spilt_word')
def spilt_word():
    return render_template('spilt_word.html')


@app.route('/spilt_word', methods=['POST'])
def get_sentence_spilt():
    input_content = request.form['sentence']
    result_list = maxMatch.get_sentence_spilt(input_content)
    result = ''
    for i in result_list:
        result += i + ' \ '
    return render_template('spilt_word.html', spilt_result=result, input_content=input_content)


@app.route('/song_ci')
def song_ci():
    return render_template('generateCi.html', recommend=generateCi.random_name(), ci_name="")


@app.route('/song_ci', methods=['POST'])
def generate():
    ci_content = generateCi.generate_ci(request.form['ci_name'])
    return render_template('generateCi.html', recommend=generateCi.random_name(), ci_content=ci_content)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
