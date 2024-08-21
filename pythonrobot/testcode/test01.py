from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/first', methods=['GET'])
def first_endpoint():
    # 处理 /first 的逻辑
    data = {'message': 'This is the first endpoint.'}

    # 调用第二个接口
    second_response = requests.get('http://127.0.0.1:5000/second')

    # 处理 second_response，例如可以将其结果包含在返回结果中
    return jsonify(data, second_response.json())


@app.route('/second', methods=['GET'])
def second_endpoint():
    # 处理 /second 的逻辑
    data = {'message': 'This is the second endpoint.'}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)