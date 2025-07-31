# 58xueke.cn
# 适配Python 3.11 + Qdrant + BGE模型的工具函数

import os
import json
from typing import List, Dict, Any
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.documents import Document

def save_chat_history(chat_history, folder_name):
    """
    将聊天记录存储到指定的文件夹下的chat_history.txt文件中。

    Args:
        chat_history (list): 聊天记录列表，每个元素是一个AIMessage或HumanMessage对象。
        folder_name (str): 聊天记录文件夹的名称。

    Returns:
        str: 保存的文件路径，如果保存失败则返回None。
    """
    try:
        file_path = os.path.join(folder_name, "chat_history.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            for message in chat_history:
                if isinstance(message, AIMessage):
                    speaker = "面试官"
                elif isinstance(message, HumanMessage):
                    speaker = "应聘者"
                else:
                    continue
                file.write(f"{speaker}: {message.content}\n")
        return file_path
    except Exception as e:
        print(f"保存聊天记录失败：{e}")
        return None


def parse_jd_to_json(llm, jd_file_path: str):
    """
    将给定的 JD 文件内容解析为 JSON，并存储到指定路径下。
    """
    try:
        with open(jd_file_path, 'r', encoding='utf-8') as jd_file:
            jd_content = jd_file.read().strip()

        template = """
基于JD文本，按照约束，生成以下格式的 JSON 数据：
{{
  "基本信息": {{
    "职位": "职位名称",
    "薪资": "薪资范围",
    "地点": "工作地点",
    "经验要求": "经验要求",
    "学历要求": "学历要求",
    "其他":""
  }},
  "岗位职责": {{
    "具体职责": ["职责1", "职责2", ...]
  }},
  "岗位要求": {{
    "学历背景": "学历要求",
    "工作经验": "工作经验要求",
   "技能要求": ["技能1", "技能2", ...],
    "个人特质": ["特质1", "特质2", ...],
  }},
  "专业技能/知识/能力": ["技能1", "技能2", ...],
  "其他信息": {{}}
}}

JD文本：
[{jd_content}]

约束：
1、除了`专业技能/知识/能力`键，其他键的值都从原文中获取。
2、保证JSON里的值全面覆盖JD原文，不遗漏任何原文，不知如何分类就放到`其他信息`里。
3、`专业技能/知识/能力`键对应的值要求从JD全文中（尤其是岗位职责、技能要求部分）提取总结关键词或关键短句，不能有任何遗漏的硬技能。

JSON：
"""
        parser = JsonOutputParser()

        prompt = PromptTemplate(
            template=template,
            input_variables=["jd_content"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | llm | parser
        result = chain.invoke({"jd_content": jd_content})

        output_file_path = "data/jd.json"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(result, output_file, ensure_ascii=False, indent=2)

        print(f"已存储最终 JSON 文件到 {output_file_path}")
        return output_file_path
    except Exception as e:
        print(f"解析 JD 文件时出错: {str(e)}")
        return None


def read_json(file_path: str) -> dict:
    """读取 JSON 文件并返回其内容。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"读取 JSON 文件时出错: {str(e)}")
        return {}


def parse_cv_to_md(llm, cv_file_path: str):
    """
    将给定的简历文件内容解析为 Markdown，并存储到指定路径下。
    """
    try:
        with open(cv_file_path, 'r', encoding='utf-8') as cv_file:
            cv_content = cv_file.read().strip()

        template = """
基于简历文本，按照约束，转换成Markdown格式：

简历文本：
[{cv_content}]

约束：
1、只用一级标题和二级标题分出来简历的大块和小块
2、一级标题只有这些：个人信息、教育经历、工作经历、项目经历、校园经历、职业技能、曾获奖项、兴趣爱好、自我评价、其他信息。

Markdown：
"""
        parser = StrOutputParser()

        prompt = PromptTemplate(
            template=template,
            input_variables=["cv_content"]
        )

        chain = prompt | llm | parser
        result = chain.invoke({"cv_content": cv_content})

        output_file_path = "data/cv.md"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(result.strip("```"))
            output_file.write("\n\n")

        print(f"已存储最终 Markdown 文件到 {output_file_path}")
        return output_file_path
    except Exception as e:
        print(f"解析 CV 文件时出错: {str(e)}")
        return None


# ========== 新增：Qdrant + BGE本地嵌入模型支持 ==========

def create_qdrant_vector_store(collection_name: str = "cv_collection"):
    """
    创建Qdrant向量存储，使用本地BGE模型
    """
    try:
        from qdrant_client import QdrantClient
        from sentence_transformers import SentenceTransformer
        from langchain_community.vectorstores import Qdrant
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        # 连接到Docker中的Qdrant
        client = QdrantClient(host="localhost", port=6333)
        
        # 使用本地BGE模型
        model_path = "./models--BAAI--bge-small-zh-v1.5"  # 您的本地模型路径
        embeddings = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs={'device': 'cpu'},  # 如果有GPU可以改为'cuda'
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # 创建Qdrant向量存储
        vector_store = Qdrant(
            client=client,
            collection_name=collection_name,
            embeddings=embeddings,
        )
        
        return vector_store, embeddings
    except Exception as e:
        print(f"创建Qdrant向量存储时出错: {str(e)}")
        return None, None


def parse_md_file_to_docs_qdrant(file_path: str, collection_name: str = "cv_collection"):
    """
    解析MD文件并存储到Qdrant向量数据库
    """
    try:
        from langchain.text_splitter import MarkdownHeaderTextSplitter
        
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_text = file.read()

        docs = []
        headers_to_split_on = [
            ("#", "Title 1"),
            ("##", "Title 2"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        split_docs = markdown_splitter.split_text(markdown_text)
        
        for split_doc in split_docs:
            metadata = split_doc.metadata
            title_str = f"# {metadata.get('Title 1', 'None')}\n## {metadata.get('Title 2', 'None')}\n"
            page_content = title_str + split_doc.page_content.strip()
            doc = Document(
                page_content=page_content,
                metadata=metadata
            )
            docs.append(doc)
        
        # 存储到Qdrant
        vector_store, _ = create_qdrant_vector_store(collection_name)
        if vector_store and docs:
            vector_store.add_documents(docs)
            print(f"成功将{len(docs)}个文档存储到Qdrant集合'{collection_name}'")
        
        return docs
    except Exception as e:
        print(f"解析MD文件到Qdrant时出错: {str(e)}")
        return []


def search_cv_content_qdrant(query: str, collection_name: str = "cv_collection", k: int = 3):
    """
    使用Qdrant搜索简历相关内容
    """
    try:
        vector_store, _ = create_qdrant_vector_store(collection_name)
        if vector_store:
            results = vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        return []
    except Exception as e:
        print(f"搜索简历内容时出错: {str(e)}")
        return []


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0,
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com"
    )

    # 测试JD解析
    # jd_file_path = "data/jd.txt"
    # result = parse_jd_to_json(llm, jd_file_path)
    # print(result)

    # 测试CV解析
    # cv_file_path = "data/cv.txt"
    # result = parse_cv_to_md(llm, cv_file_path)
    # print(result)
    
    # 测试Qdrant向量存储
    # parse_md_file_to_docs_qdrant("data/cv.md")
    # results = search_cv_content_qdrant("Python开发经验")
    # print(results)
