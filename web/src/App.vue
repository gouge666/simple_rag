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
        <!-- 管理按钮 -->
        <button v-if="is_chatting_page" @click="is_chatting_page = false">
          管理
        </button>
        <button v-else @click="is_chatting_page = true">返回</button>
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
    <div class="right-content" v-show="is_chatting_page">
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
    <div class="right-content" v-show="!is_chatting_page">
      <div class="delete-container">
        <button @click="deleteKnowledge" class="delete-btn">删除</button>
      </div>
      <div class="segment-list">
        <div
          v-for="(item, index) in all_segments_data.documents"
          :key="index"
          class="segment-item"
        >
          <div class="item-index">
            知识片段id:{{ all_segments_data.ids[index] }}
          </div>
          <div class="item-content">
            <textarea
              v-model="editedItems[index]"
              @blur="saveEdit(index)"
              class="edit-textarea"
              >{{ item }}</textarea
            >
          </div>
          <div class="action-buttons">
            <button @click="deleteSegment(index)" class="delete-segment-btn">
              删除
            </button>
            <button @click="saveSegment(index)" class="save-segment-btn">
              保存
            </button>
          </div>
        </div>
      </div>
      <div class="add-new-container">
        <textarea
          v-model="newKnowledge"
          placeholder="输入新知识"
          class="add-textarea"
        ></textarea>
        <button @click="add_new_segments" class="add-btn">添加</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面主体的字体设置 */
body {
  font-family: "Roboto", sans-serif;
  background-color: #f8f9fa;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #e9ecef;
}

::-webkit-scrollbar-thumb {
  background: #868e96;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6c757d;
}

/* 选择知识库部分的样式 */
.select-knowledge {
  margin-bottom: 30px;
}

.select-knowledge:hover {
  cursor: pointer;
}

.select-knowledge option:hover {
  background-color: #dee2e6;
}

/* 整个页面容器的样式 */
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
}

/* 左侧侧边栏的样式 */
.left-sidebar {
  width: 300px;
  background-color: #f1f3f5;
  padding: 30px;

  label {
    font-size: 20px;
    font-weight: 500;
    margin-bottom: 20px;
    color: #343a40;
  }

  select {
    width: 100%;
    padding: 15px;
    font-size: 18px;
    border-radius: 10px;
    border: 2px solid #adb5bd;
    background-color: #fff;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .create-knowledge h3 {
    font-size: 24px;
    margin-top: 30px;
    color: #343a40;
  }

  input[type="text"] {
    width: 100%;
    padding: 15px;
    font-size: 18px;
    border-radius: 10px;
    border: 2px solid #adb5bd;
    background-color: #fff;
    margin-top: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  input[type="file"] {
    margin-top: 20px;
  }

  button {
    width: 100%;
    padding: 20px;
    font-size: 20px;
    color: #fff;
    background: linear-gradient(to bottom right, #4caf50, #388e3c);
    border: none;
    border-radius: 10px;
    cursor: pointer;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    margin-top: 30px;
  }
}

/* 右侧内容区域的样式 */
.right-content {
  flex: 1;
  padding: 30px;
  background-color: #fff;
  display: flex;
  flex-direction: column;

  .chat-history {
    height: calc(100vh - 180px);
    overflow-y: auto;
    background-color: #f8f9fa;
    margin-bottom: 50px;

    .chat-item {
      margin-bottom: 30px;
      padding: 0 30px;

      .robot-message {
        .message-content {
          background-color: #e9ecef;
          padding: 30px;
          border-radius: 20px;
          font-size: 20px;
          display: inline-block;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
      }

      .user-message {
        text-align: right;
        .message-content {
          background-color: #86c232;
          padding: 30px;
          border-radius: 20px;
          font-size: 20px;
          display: inline-block;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
      }
    }
  }

  .chat-input {
    display: flex;

    textarea {
      flex: 1;
      padding: 25px;
      font-size: 20px;
      border-radius: 20px;
      border: 4px solid #4caf50;
      box-shadow: 0 4px 6px rgba(76, 175, 80, 0.5);
      resize: none;
    }

    button {
      padding: 25px 50px;
      font-size: 20px;
      color: #fff;
      background: linear-gradient(to bottom right, #4caf50, #388e3c);
      border: none;
      border-radius: 20px;
      cursor: pointer;
      box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
  }

  .right-content h2 {
    font-size: 28px;
    margin-bottom: 30px;
    color: #343a40;
  }

  .delete-container {
    margin-bottom: 30px;
  }

  .delete-btn {
    padding: 10px 20px;
    width: 150px;
    height: 40px;
    background-color: #dc3545;
    color: #fff;
    border-radius: 10px;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  }

  .segment-list {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    height: calc(100vh - 180px);
    overflow: hidden;
    overflow-y: auto;
  }

  .segment-item {
    padding: 25px;
    border-bottom: 1px solid #dee2e6;
  }

  .item-index {
    font-weight: 500;
    margin-right: 20px;
    color: #343a40;
  }

  .item-content {
    padding-left: 20px;
  }

  .edit-textarea {
    width: 100%;
    height: 150px;
    resize: vertical;
    padding: 15px;
    font-size: 18px;
    border-radius: 10px;
    border: 2px solid #adb5bd;
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .action-buttons {
    margin-top: 15px;
  }

  .delete-segment-btn,
  .save-segment-btn {
    padding: 10px 20px;
    margin-right: 15px;
    border-radius: 10px;
    font-size: 18px;
    cursor: pointer;
  }

  .delete-segment-btn {
    background-color: #dc3545;
    color: #fff;
  }

  .save-segment-btn {
    background-color: #28a745;
    color: #fff;
  }

  .add-new-container {
    display: flex;
    height: 60px;
    margin-top: 30px;
  }

  .add-textarea {
    width: 100%;
    height: 60px;
    resize: vertical;
    padding: 15px;
    font-size: 18px;
    border-radius: 10px;
    border: 2px solid #adb5bd;
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .add-btn {
    width: 100px;
    background-color: #17a2b8;
    color: #fff;
    border-radius: 10px;
    cursor: pointer;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  }
}
</style>

<script setup>
// 导入 Vue 相关的模块
import { ref, onMounted, watch } from "vue";

const is_chatting_page = ref(true);
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
        });
      });
    });
  }
};

// 删除知识库的方法，需要用户确认
const deleteKnowledge = () => {
  // 弹出确认删除的提示
  if (confirm("确定要删除该知识库吗？")) {
    // 创建表单数据对象
    var formData = new FormData();
    // 向表单数据中添加数据
    formData.append("db_name", db_name.value);

    // 发送删除知识库的请求
    fetch("/api/delete_chroma_db", {
      method: "POST",
      body: formData,
    }).then((response) => {
      // 如果响应不成功，抛出错误
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      // 弹出删除成功的提示
      alert("删除成功");
      // 更新知识库列表
      fetch("/api/knowledge_list", { method: "GET" }).then((response) => {
        // 如果响应不成功，抛出错误
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        is_chatting_page.value = true;
        // 将响应数据转换为 JSON 格式，并更新 knowledgeList 数据
        response.json().then((data) => {
          knowledgeList.value = data;
          db_name.value = data[0];
        });
      });
    });
  }
};

const all_segments_data = ref({
  documents: [],
});
// 初始化一个新的数组来存储编辑的值
const editedItems = ref([]);

// 编辑和保存的相关方法
const saveEdit = (index) => {
  all_segments_data.value.documents[index] = editedItems.value[index];
};

const saveSegment = (index) => {
  var formData = new FormData();
  // 向表单数据中添加数据
  formData.append("db_name", db_name.value);
  formData.append("id", all_segments_data.value.ids[index]);
  formData.append("new_content", editedItems.value[index]);
  formData.append(
    "metedata_source",
    all_segments_data.value.metadatas[index].source
  );
  fetch("/api/update_segments_by_id", {
    method: "POST",
    body: formData,
  }).then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    // 提示保存成功
    alert("保存成功");
  });
};

const deleteSegment = (index) => {
  if (confirm("确定要删除该片段吗？")) {
    var formData = new FormData();
    // 向表单数据中添加数据
    formData.append("db_name", db_name.value);
    formData.append("id", all_segments_data.value.ids[index]);
    fetch("/api/delete_segments_by_id", {
      method: "POST",
      body: formData,
    }).then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      // 提示删除成功
      alert("删除成功");
      get_all_fragments();
    });
  }
};
const newKnowledge = ref("");

const add_new_segments = () => {
  var formData = new FormData();
  // 向表单数据中添加数据
  formData.append("db_name", db_name.value);
  formData.append("new_content", newKnowledge.value);
  formData.append("metedata_source", "手动添加");
  fetch("/api/add_new_segments", {
    method: "POST",
    body: formData,
  }).then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    newKnowledge.value = "";
    // 提示保存成功
    alert("保存成功");
    get_all_fragments();
  });
};
// 获取全部片段
const get_all_fragments = () => {
  var formData = new FormData();
  // 向表单数据中添加数据
  formData.append("db_name", db_name.value);
  fetch("/api/get_all_segments", {
    method: "POST",
    body: formData,
  }).then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    response.json().then((data) => {
      console.log(data);
      all_segments_data.value = data;
      editedItems.value = data.documents.map((item) => item);
    });
  });
};
watch(db_name, () => {
  console.log(db_name.value);
  get_all_fragments();
});
</script>
