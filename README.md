以下是为您调整格式后的 README 文件：

```markdown
# 项目启动指南

## Python 后端启动步骤

1. 创建新环境
    ```
    conda create -n rag_system python=3.12
    ```
2. 激活环境
    ```
    conda activate rag_system
    ```
3. 安装后端依赖
    ```
    pip install -r requirement.txt
    ```
4. 启动后端程序
    ```
    python app.py
    ```

**注意**：如果启动过程中出现报错，若是缺少某些模块，使用 `pip` 安装即可。若无法连外网下载 `text2vec-large-chinese` ，可去 `modelscope` 手动下载后放到根目录。

## Web 页面启动步骤

1. 进入 `web` 目录
    ```
    cd web
    ```
2. 确认是否安装 `Node.js` ，使用 `node -V` 命令查看，出现版本号说明已安装，未出现则需先安装 `Node.js` 。
3. 安装 `web` 项目依赖
    ```
    npm i
    ```
4. 启动网页
    ```
    npm run dev
    ```
```

您觉得这个格式是否符合您的需求？如果您还有其他要求，比如添加更多的说明或者修改语言表述，都可以随时告诉我。
