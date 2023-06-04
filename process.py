import os

# Import langchain lib
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.chains.question_answering import load_qa_chain

def load_pdf(pdf_path):
	loader = UnstructuredPDFLoader(pdf_path)
	pages = loader.load()
	return pages

def update_openai_key(openai_key):
	os.environ['OPENAI_API_KEY'] = openai_key

def texts_splitter(pages):
	text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=20)
	texts = text_splitter.split_documents(pages)
	return texts

def qa_langchain(docsearch):
	qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
	qa = RetrievalQA(combine_documents_chain=qa_chain, retriever=docsearch.as_retriever())
	return qa

def main_process(pdf_path, question, openai_key):
	# Update OpenAI key
	update_openai_key(openai_key)
	# load PDF
	pages = load_pdf(pdf_path)
	# Text splitter
	texts = texts_splitter(pages)

	# define embeddings
	embeddings = OpenAIEmbeddings()
	# print(embeddings)
	docsearch = Chroma.from_documents(texts, embeddings)

	qa = qa_langchain(docsearch)
	answer = qa.run(question)
	return answer
