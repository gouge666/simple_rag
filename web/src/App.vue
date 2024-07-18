<template>
  <!-- 整个页面的容器，设置了阴影效果 -->
  <div class="container" style="box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)">
    <!-- 左侧侧边栏，设置了阴影效果 -->
    <div class="left-sidebar" style="box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)">
      <!-- 选择知识库的部分 -->
      <div class="select-knowledge">
        <!-- 选择知识库的标签 -->
        <label
          for="knowledge"
          style="
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
          "
          >选择知识库</label
        >
        <!-- 知识库的下拉选择框，通过 v-model 与数据进行双向绑定 -->
        <select v-model="db_name">
          <!-- 通过 v-for 循环生成选项 -->
          <option
            v-for="(item, index) in knowledgeList"
            :key="index"
            :value="item"
          >
            {{ item }}
          </option>
        </select>
      </div>

      <!-- 创建知识库的部分 -->
      <div class="create-knowledge">
        <!-- 创建知识库的标题 -->
        <h3 style="font-size: 20px; margin-top: 20px">创建知识库</h3>
        <!-- 输入知识库名称的输入框，通过 v-model 与数据进行双向绑定 -->
        <input
          type="text"
          placeholder="知识库名称"
          v-model="new_db_name"
          style="font-size: 16px"
        />
        <!-- 文件选择输入框，接受特定格式的文件 -->
        <input
          type="file"
          accept=".docx,.pdf,.txt"
          @change="handleFileChange"
        />
        <!-- 创建按钮，根据条件判断是否禁用，点击时触发 createKnowledge 方法 -->
        <button
          @click="createKnowledge"
          :disabled="!new_db_name || !selectedFile"
        >
          创建
        </button>
      </div>
    </div>
    <!-- 右侧内容区域 -->
    <div class="right-content">
      <!-- 聊天历史记录部分 -->
      <div class="chat-history">
        <!-- 通过 v-for 循环展示每条聊天记录 -->
        <div v-for="(item, index) in msgList" :key="index" class="chat-item">
          <!-- 如果消息角色是机器人 -->
          <div v-if="item.role === 'robot'" class="robot-message">
            <!-- 显示机器人消息的时间 -->
            <p style="font-size: 14px; color: #888; margin-bottom: 5px">
              {{ item.time }}
            </p>
            <!-- 机器人消息的内容 -->
            <div
              class="message-content"
              style="
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                display: inline-block;
              "
            >
              {{ item.content }}
            </div>
          </div>
          <!-- 如果消息角色是用户 -->
          <div v-else class="user-message">
            <!-- 显示用户消息的时间 -->
            <p
              style="
                font-size: 14px;
                color: #888;
                margin-bottom: 5px;
                text-align: right;
              "
            >
              {{ item.time }}
            </p>
            <!-- 用户消息的内容 -->
            <div
              class="message-content"
              style="
                background-color: #90ee90;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                display: inline-block;
              "
            >
              {{ item.content }}
            </div>
          </div>
        </div>
      </div>
      <!-- 聊天输入部分 -->
      <div class="chat-input">
        <!-- 输入聊天消息的文本框，通过 v-model 与数据进行双向绑定 -->
        <textarea
          v-model="query"
          type="text"
          placeholder="Type a message..."
          style="font-size: 16px"
        ></textarea>
        <!-- 发送消息的按钮，根据条件判断是否禁用，点击时触发 sendMsg 方法 -->
        <button @click="sendMsg" :disabled="!query">
          <!-- 如果正在发送消息，显示加载动画 -->
          <span v-if="sendingMessage">
            <svg width="20" height="20" viewBox="0 0 24 24">
              <circle
                cx="12"
                cy="12"
                r="10"
                fill="none"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-dasharray="120 120"
                stroke-dashoffset="0"
                transform="rotate(-90 12 12)"
              ></circle>
            </svg>
          </span>
          <!-- 否则显示发送按钮文字 -->
          <span v-else>Send</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面主体的字体设置 */
body {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 选择知识库部分的样式 */
.select-knowledge {
  margin-bottom: 25px;
}

.select-knowledge:hover {
  cursor: pointer;
}

.select-knowledge option:hover {
  background-color: #ddd;
}

/* 整个页面容器的样式 */
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #fafafa;
}

/* 左侧侧边栏的样式 */
.left-sidebar {
  width: 300px;
  background-color: #e8e8e8;
  padding: 25px;

  label {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #555;
  }

  select {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border-radius: 8px;
    border: 2px solid #ccc;
    background-color: #fff;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .create-knowledge h3 {
    font-size: 22px;
    margin-top: 25px;
    color: #555;
  }

  input[type="text"] {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border-radius: 8px;
    border: 2px solid #ccc;
    background-color: #fff;
    margin-top: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  input[type="file"] {
    margin-top: 15px;
  }

  button {
    width: 100%;
    padding: 15px;
    font-size: 18px;
    color: #fff;
    background: linear-gradient(to bottom right, #4caf50, #388e3c);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    margin-top: 25px;
  }
}

/* 右侧内容区域的样式 */
.right-content {
  flex: 1;
  padding: 25px;
  background-color: #fafafa;

  .chat-history {
    height: calc(100vh - 150px);
    overflow-y: auto;
    background-color: #fff;
    margin-bottom: 40px;

    .chat-item {
      margin-bottom: 25px;
      padding: 0 25px;

      .robot-message {
        .message-content {
          background-color: #f0f0f0;
          padding: 25px;
          border-radius: 15px;
          font-size: 18px;
          display: inline-block;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
      }

      .user-message {
        text-align: right;
        .message-content {
          background-color: #90ee90;
          padding: 25px;
          border-radius: 15px;
          font-size: 18px;
          display: inline-block;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
      }
    }
  }

  .chat-input {
    display: flex;

    textarea {
      flex: 1;
      padding: 20px;
      font-size: 18px;
      border-radius: 15px;
      border: 3px solid #4caf50;
      box-shadow: 0 2px 4px rgba(76, 175, 80, 0.5);
      resize: none;
    }

    button {
      padding: 20px 40px;
      font-size: 18px;
      color: #fff;
      background: linear-gradient(to bottom right, #4caf50, #388e3c);
      border: none;
      border-radius: 15px;
      cursor: pointer;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
  }
}
</style>

<script setup>
// 导入 Vue 相关的模块
import { ref, onMounted } from "vue";

// 在页面挂载时执行的函数
onMounted(() => {
  // 发送获取知识库列表的请求
  fetch("/api/knowledge_list", { method: "GET" }).then((response) => {
    // 如果响应不成功，抛出错误
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    // 将响应数据转换为 JSON 格式，并更新 knowledgeList 数据
    response.json().then((data) => {
      knowledgeList.value = data;
      db_name.value = data[0];
    });
  });
});
// 用于标识是否正在发送消息的变量
const sendingMessage = ref(false);

// 聊天消息列表
const msgList = ref([
  {
    role: "robot",
    time: "2024/7/17 22:59:57",
    content: "你好我的主人，有什么我可以帮助你的吗？",
  },
]);

// 知识库列表
const knowledgeList = ref([]);
// 当前选择的知识库名称
const db_name = ref("");
// 用户输入的查询内容
const query = ref("");

// 发送消息的方法
const sendMsg = () => {
  // 如果用户输入了内容
  if (query.value) {
    // 将用户输入的消息添加到消息列表
    msgList.value.push({
      role: "me",
      time: new Date().toLocaleString(),
      content: query.value,
    });

    // 创建表单数据对象
    var formData = new FormData();

    // 向表单数据中添加数据
    formData.append("db_name", db_name.value);
    formData.append("question", query.value);

    // 初始化机器人回复的消息
    msgList.value.push({
      role: "robot",
      time: new Date().toLocaleString(),
      content: "",
    });

    // 发送请求，并处理响应
    fetch("/api/query", {
      method: "POST",
      dataType: "text/event-stream",
      body: formData,
    })
      .then((response) => {
        // 如果响应不成功，抛出错误
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        // 获取可读流
        return response.body;
      })
      .then((body) => {
        // 获取可读流的读取器
        const reader = body.getReader();
        // 定义读取数据的函数
        function read() {
          return reader.read().then(({ done, value }) => {
            // 如果读取完成
            if (done) {
              console.log("已传输完毕");
              return;
            }
            // 解码数据
            const decoder = new TextDecoder("utf-8");
            const decodedString = decoder.decode(value);
            // 处理接收到的数据
            console.log("收到的数据:", decodedString);
            msgList.value[msgList.value.length - 1].content += decodedString;
            // 继续读取
            read();
          });
        }
        // 开始读取数据
        read();
      });

    // 清空用户输入的内容
    query.value = "";
  }
};

// 选中文件时触发的函数
const selectedFile = ref(null);
const handleFileChange = (e) => {
  selectedFile.value = e.target.files[0];
  console.log(selectedFile.value);
};

// 创建知识库的方法
const new_db_name = ref("");
const createKnowledge = () => {
  // 如果输入了知识库名称并且选择了文件
  if (new_db_name.value && selectedFile.value) {
    // 创建表单数据对象
    var formData = new FormData();
    // 向表单数据中添加数据
    formData.append("db_name", new_db_name.value);
    formData.append("source", selectedFile.value);

    // 发送创建知识库的请求
    fetch("/api/create_chroma_db", {
      method: "POST",
      body: formData,
    }).then((response) => {
      // 如果响应不成功，抛出错误
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      // 清空输入的知识库名称和选中的文件
      new_db_name.value = "";
      selectedFile.value = null;
      // 弹出创建成功的提示
      alert("创建成功");
      // 更新知识库列表
      fetch("/api/knowledge_list", { method: "GET" }).then((response) => {
        // 如果响应不成功，抛出错误
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        // 将响应数据转换为 JSON 格式，并更新 knowledgeList 数据
        response.json().then((data) => {
          knowledgeList.value = data;
          db_name.value = data[0];
        });
      });
    });
  }
};
</script>
