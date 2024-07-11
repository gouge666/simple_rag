from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="xxx",
    model='qwen2-72b-instruct',
    temperature=0,
)

