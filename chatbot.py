from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
persist_directory = 'vectordb'
folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

print("I do think I have a db", db)
retriever = db.as_retriever()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

def chatbot (query):
	while True:
    		answer = qa.run(query)
    		return answer
