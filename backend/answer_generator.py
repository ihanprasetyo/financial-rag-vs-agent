# backend/answer_generator.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#"gpt-3.5-turbo"
def generate_answer(question, chunks, model="gpt-3.5-turbo"):
    prompt = f"""You are a financial analyst. Use the context below to answer the question. Be concise and accurate.

Question: {question}

Context:
{chr(10).join(chunks)}

Answer:"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content