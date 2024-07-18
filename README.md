启动python写的后端

创建一个新的环境
conda create -n rag_system python=3.12
激活环境
conda activate rag_system
安装python后端依赖
pip install -r requirement.txt
启动后端程序
python app.py

如果出现报错，如果是缺少某些模块，pip一下就行，如果不能连外网，下载不了 text2vec-large-chinese，可以去 modelscope 手动下载后放到根目录就行

启动 web 页面
进入 web 目录
cd web
保证安装过 node.js,使用 node -V 命令查看，出现版本号说明安装过，没有出现需要先安装 node.js
node -V
安装 web 项目依赖
npm i
启动网页
npm run dev



