from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationChain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

persist_directory = 'vectordb'
#folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer')
print("I do think I have a db", db)
retriever = db.as_retriever()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
#qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever,memory=memory)
while True:
    query = input("> ")
    if query =="clear memory":
        memory.clear()
        answer = "I've wiped our conversation"
    else: 
        answer = qa.run({"question": query,"chat_history": ConversationBufferMemory()})
 
    print(answer)
#def chatbot (query):
#    while True:
#        if query == "clear memory":
#            memory.clear()
#            answer = "I've wiped our conversation"
#        else:
#            answer = qa.run({"question": query, "chat_history": ConversationBufferMemory()})


#        return answer
