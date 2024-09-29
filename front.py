import streamlit as st
import requests

st.title("PDF Q&A")

if 'history' not in st.session_state:
    st.session_state['history'] = []

uploaded_file = st.file_uploader("Upload PDF", accept_multiple_files=False, type=["pdf"])

if uploaded_file:    
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post("http://127.0.0.1:5000/upload", files=files)
    
    if response.status_code != 200:
        st.write("Error uploading file")
    else:
        st.write("File uploaded and processed.")

    query = st.text_input("Type a query.")
    
    if query:
        query_data = {"question": query}
        query_response = requests.post("http://127.0.0.1:5000/query", json=query_data)
        
        if query_response.status_code == 200:
            result = query_response.json()
            answer = result.get("result", "No result returned")
            
            st.session_state['history'].append({"question": query, "answer": answer})

            st.write("Result:")
            st.write(answer)
        else:
            st.error(f"API returned an error: {query_response.status_code}")
            st.write(query_response.text)

st.subheader("History")
with st.container():
    for item in st.session_state['history']:
        with st.expander(f"Question: {item['question']}"):
            st.write(f"Answer: {item['answer']}")