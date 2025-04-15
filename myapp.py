import streamlit as st
import os 
from dotenv import load_dotenv

from langchain_groq import ChatGroq 
st.title("RAG DOCUMENT SUMMARIZER 📁⏺️")
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document 

load_dotenv()


# from docx import Document
uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
file_text=''
final_documents=[]
def pdf_to_documents(pdf_file):
    """Extracts text from a PDF and converts it into LangChain Document format."""
    # pdf_reader = PdfReader(pdf_file)
    documents = []

    for i, page in enumerate(pdf_file.pages):
        text = page.extract_text()
        if text:
            doc = Document(
                page_content=text,  # The actual text of the PDF page
                # metadata={"source": pdf_file.name, "page": i + 1}  # Metadata for tracking
            )
            documents.append(doc)

    return documents
if uploaded_file is not None:
    st.success("File uploaded successfully!")
    pdf_reader = PdfReader(uploaded_file)


    pdf_to_doc=pdf_to_documents(pdf_reader)
# file_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    final_documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(pdf_to_doc)


# final_documents = [Document(page_content=chunk) for chunk in final_documents]  

llm=ChatGroq(groq_api_key="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",model="gemma2-9b-it")


# final_documents=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=100).split_documents(uploaded_file)
##Defining prompts 
from langchain_core.prompts import PromptTemplate
chunk_prompt='''You are an expert summarizer. Summarize the following passage while preserving key details and important concepts. Avoid unnecessary repetition.

Passage:
{text}

'''

chunk_prompt_template=PromptTemplate(input_variables=['text'],template=chunk_prompt)

final_prompt='''Here are summaries of different sections of a document. Generate a final, concise summary that maintains coherence and preserves the most critical details.

Section Summaries:
{text}'''

final_prompt_template=PromptTemplate(input_variables=['text'],template=final_prompt)

# Summarizing the doc

from langchain.chains.summarize import load_summarize_chain

chain=load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",
    map_prompt=chunk_prompt_template,
    combine_prompt=final_prompt_template,
    verbose=True
)

if final_documents is not None:
    if st.button('Summarize the document'):
        st.write(chain.run(final_documents))

    

