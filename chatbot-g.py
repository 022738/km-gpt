from langchain.llms import VertexAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationChain

persist_directory = 'gvectordb'
#folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
embeddings = VertexAIEmbeddings()
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

print("I do think I have a db", db)
retriever = db.as_retriever()

llm = VertexAI(temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
chat_history=[]
while True:
    query = input("> ")
    answer = qa.run({"question": query,"chat_history": chat_history})
    chat_history = [(query, answer)] 
    print(answer)

#def chatbot (query):
#	while True:
#    		answer = qa.run(query)
#    		return answer
