import os

from my_llm import llm
from langchain_community.document_loaders import TextLoader,PyPDFium2Loader,CSVLoader,Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(
    model_name="GanymedeNil/text2vec-large-chinese", cache_folder="./text2vec-large-chinese"
)


def create_chroma_db(db_name, temp_source_file_path):
    persist_directory = "./dbs/" + db_name
    # 获取文件扩展名以决定使用哪一个Loader
    extension = temp_source_file_path.split(".")[-1]
    loader = None
    if extension == 'txt':
        loader = TextLoader(temp_source_file_path,encoding='utf8')
    if extension == 'pdf':
        loader = PyPDFium2Loader(temp_source_file_path)
    if extension == 'docx':
        loader = Docx2txtLoader(temp_source_file_path)

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_directory)
    # 删除临时文件
    try:
        os.remove(temp_source_file_path)
    except Exception as e:
        print(f"Error deleting temporary file: {e}")

    return "ok"


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def answer_user_query(db_name, question):
    persist_directory = "./dbs/" + db_name
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    retriever = vectorstore.as_retriever()

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "指出用户的问题是什么,你的答案是什么？不知道的回答不知道就行，回答需要有理有据。"),
            ("user", "我的问题是:{question}，\n可参考以下内容：{context}")
        ]
    )

    return llm.stream(prompt_template.invoke(
        {"context": format_docs(retriever.invoke(question)), "question": question}
    ).to_messages())