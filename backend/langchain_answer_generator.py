# backend/langchain_answer_generator.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    temperature=0.3,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="""You are a financial analyst. Use the context below to answer the question. Be concise and accurate.

Question: {question}

Context:
{context}

Answer:"""
)

chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_answer_lc(question, chunks):
    context = "\n".join(chunks)
    return chain.run({"question": question, "context": context})