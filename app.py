from flask import Flask, request
import time
import os
from flask import stream_with_context
from db_operation import create_chroma_db as create_db, answer_user_query

app = Flask(__name__)

def ensure_dir(f):

    """确保目录存在"""

    dir = os.path.dirname(f)

    if not os.path.exists(dir):

        os.makedirs(dir)

@app.route("/create_chroma_db", methods=['POST'])
def create_chroma_db():

    db_name = request.form['db_name']

    source_file = request.files['source']

    source_file_temp_save_path = str(time.time()) + source_file.filename

    # 保存文件到指定目录

    basedir = os.path.abspath(os.path.dirname(__file__)) # 当前文件夹路径

    filepath = os.path.join(basedir, 'uploads', source_file_temp_save_path) # uploads是存放文件的子目录

    ensure_dir(filepath) # 确保目录存在

    source_file.save(filepath)

    print(source_file_temp_save_path)

    return create_db(db_name, filepath)


@app.route("/knowledge_list", methods=['GET'])
def knowledge_list():
    #  指定目录路径
    directory_path = 'dbs'

    #  获取目录下的所有文件和文件夹
    entries = os.listdir(directory_path)

    #  过滤出文件夹
    subdirectories = [d for d in entries if os.path.isdir(os.path.join(directory_path, d))]

    #  返回子目录的名称列表
    return subdirectories

@app.route("/query", methods=['POST'])
def query():
    print(request.data)
    print(request.form)
    db_name = request.form['db_name']
    question = request.form['question']

    def generate_chunks():
        for chunk in answer_user_query(db_name=db_name, question=question):
            yield chunk.content

    return stream_with_context(generate_chunks())



# 启动一个本地开发服务器，激活该网页

app.run(host="0.0.0.0", port=6666)