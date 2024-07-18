from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-7bbf11ecab944cc88c76926be754ee61",
    model='qwen2-72b-instruct',
    temperature=0,
)

