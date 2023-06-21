from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import logging

persist_directory = 'vectordb'
folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
#folder_id="19vnINFNPgJlX5xMuMAGxjXlElSF-Odas"
logging.basicConfig(filename='output.txt', level=logging.INFO, format='')
embeddings = OpenAIEmbeddings()



loader = GoogleDriveLoader(
    folder_id=folder_id,
    recursive=True
    )
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"]
     )
texts = text_splitter.split_documents(docs)
#    embeddings = OpenAIEmbeddings()
db =Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory) 

print("completed loading", db)


logging.info('Completed build')
