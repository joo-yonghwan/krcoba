from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import re

app = Flask(__name__)

statistics = {
    'numbers': defaultdict(int),
    'operators': defaultdict(int),
    'calculations': 0
}

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        numbers = re.findall(r'\d', expression)
        for num in numbers:
            statistics['numbers'][num] += 1

        operators = re.findall(r'[\+\-\*/]', expression)
        for op in operators:
            statistics['operators'][op] += 1

        statistics['calculations'] += 1

        result = eval(expression)
        return jsonify({'result': result, 'error': None})
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

@app.route('/statistics', methods=['GET'])
def get_statistics():
    return jsonify({
        'numbers': dict(statistics['numbers']),
        'operators': dict(statistics['operators']),
        'calculations': statistics['calculations']
    })

if __name__ == '__main__':
    app.run(debug=True)
