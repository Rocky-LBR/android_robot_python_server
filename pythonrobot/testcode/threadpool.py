from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor
import time


app = Flask(__name__)

# 创建一个线程池，最多允许5个线程后面修改为使用redis进行线程池建立
executor = ThreadPoolExecutor(max_workers=5)
completed_tasks = []

#封装数据库操作
def sql_test(sql,task_id):
    time.sleep(10)


#主要核心算法、耗时任务
def fetch_data(task_id):
    # 模拟一个耗时的任务
    time.sleep(2)  # 模拟网络请求
    sql_test("select * from user where id =%d"%(task_id),task_id)
    completed_tasks.append(task_id)


#建立一个api，访问后自动获取task_id将具体的任务扔进线程池中进行运行
@app.route('/start_task', methods=['POST'])
def start_task():
    if request.is_json:
        data = request.get_json()
        if 'message' in data and 'task_id' in data:
            executor.submit(fetch_data, data["task_id"])
            return jsonify({"received_message":data['message'],"message": f"Task {data['task_id']} started!"}),200
        else:
            return jsonify({"error":"Missing 'message' in JSON data"}),400
    else:
        return jsonify({"error":"Request must be JSON"}),415
@app.route('/completed_tasks', methods=['GET'])
def get_completed_tasks():
    return jsonify({"completed_tasks": completed_tasks}), 200

if __name__ == '__main__':
    app.run(debug=True)