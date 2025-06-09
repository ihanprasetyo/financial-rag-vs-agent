# backend/chunking.py

import os
from typing import List

def load_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def load_and_chunk(path: str) -> List[str]:
    text = load_text_file(path)
    return chunk_text(text)