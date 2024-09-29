import os
import pymupdf as pd
import google.generativeai as genai
from dotenv import load_dotenv

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
MODEL_ID = "models/text-embedding-004"

def chunk_text(text, k):
    print("Creating chunks...")
    chunk_list= [text[i:i+k] for i in range(0, len(text), k)]
    return chunk_list

def generateResponse(query, chunks):
    print("Formulating reponse.")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    context = " ".join(chunks)
    prompt = f"The query given by the user follows after the colon: {query}\n"
    rules = "Strictly use the following text as the database only to generate responses for the previous query. Strictly do not use your own database or knowledge about the query. The response length should be directly proportional to the number of relevant chunks. The text will follow after this colon:\n"
    search_prompt = prompt + rules + context
    response = model.generate_content(search_prompt)
    return response.text

def scrape_text(file_path):
    doc=pd.open(file_path)
    text=""
    for page in doc:
        t=page.get_text()
        text=text+t
    return text

def main(text, q):
    chunks=chunk_text(text, 500)
    ans=generateResponse(q, chunks)
    print(ans)
    return ans