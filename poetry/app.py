from flask import Flask, request, jsonify, render_template
import json
import random
import os

app = Flask(__name__)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
WUYAN_FILE = os.path.join(DATA_DIR, 'wuyan.json')
QIYAN_FILE = os.path.join(DATA_DIR, 'qiyan.json')

with open(WUYAN_FILE, encoding='utf-8') as f:
    wuyan = json.load(f)
with open(QIYAN_FILE, encoding='utf-8') as f:
    qiyan = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/poem')
def get_poem():
    poem_type = request.args.get('type', 'wuyan')
    if poem_type == 'wuyan':
        poem = random.choice(wuyan)
    elif poem_type == 'qiyan':
        poem = random.choice(qiyan)
    else:
        return jsonify({'error': 'type参数只能为wuyan或qiyan'}), 400
    print(f"[调试] 生成诗句（{poem_type}）：{poem}")
    return jsonify({'type': poem_type, 'poem': poem})

@app.route('/api/check', methods=['POST'])
def check_guess():
    data = request.get_json()
    answer = data.get('answer', '')
    guess = data.get('guess', '')
    if not answer or not guess or len(answer) != len(guess):
        return jsonify({'error': '答案和猜测长度不符'}), 400
    result = []
    answer_chars = list(answer)
    guess_chars = list(guess)
    used = [False] * len(answer_chars)
    # 先标记绿色
    for i, (g, a) in enumerate(zip(guess_chars, answer_chars)):
        if g == a:
            result.append('green')
            used[i] = True
        else:
            result.append('')
    # 再标记黄色和灰色
    for i, g in enumerate(guess_chars):
        if result[i] == 'green':
            continue
        found = False
        for j, a in enumerate(answer_chars):
            if not used[j] and g == a:
                found = True
                used[j] = True
                break
        result[i] = 'yellow' if found else 'gray'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True) 