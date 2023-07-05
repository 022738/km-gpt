from langchain.llms import VertexAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

persist_directory = 'gvectordb'
#folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
embeddings = VertexAIEmbeddings()
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer')
print("I do think I have a db", db)
retriever = db.as_retriever()

llm = VertexAI(temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever,
        memory=memory, return_source_documents=True)

#while True:
#    query = input("> ")
#    if query =="clear memory":
#        memory.clear()
#        answer = "I've wiped our conversation"
#    else: 
#        answer = qa.run({"question": query,"chat_history": ConversationBufferMemory()})
 
#    print(answer)

def chatbot_g (query):
 
    while True:
      
        if query == "clear memory":
            memory.clear()
            answer = "I've wiped our conversation"
        else:
            try:
                answer = qa({"question": query, "chat_history": ConversationBufferMemory()})
                formattedanswer = answer['answer'] + "\nTitle: " +  answer['source_documents'][0].metadata['title'] + "\nFile url: " +  answer['source_documents'][0].metadata['source'] 
            except Exception as err:
                answer = "An error occurred. Context: "+err.message
        return answer
