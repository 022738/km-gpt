from langchain.llms import VertexAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
#from langchain.chains.qa_with_sources import load_qa_with_sources_chain

persist_directory = 'gvectordb'
#folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
embeddings = VertexAIEmbeddings()
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer')
print("I do think I have a db", db)
retriever = db.as_retriever()

llm = VertexAI(temperature=0)
#doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever,memory=memory, return_source_documents=True)

while True:
    query = input("> ")
    if query =="clear memory":
        memory.clear()
        answer = "I've wiped our conversation"
    else:
        try:

            answer = qa({"question": query,"chat_history": ConversationBufferMemory()})
        except Exception as err:
            print (err)
            print (err.message)
    print(answer['answer'])
    print(answer['source_documents'][0].metadata['source'])

    formattedanswer = answer['answer'] + "\nTitle:  " +  answer['source_documents'][0].metadata['title'] + "File url: " +  answer['source_documents'][0].metadata['source'] 
    print(formattedanswer)
#def chatbot_g (query):
   # chat_history=[]
 #   while True:
       # memory.save_context({"input": "hi"}, {"output": "whats up"})
        #answer = qa.run({"question": query,"chat_history": chat_history})
  #      if query == "clear memory":
   #        memory.clear()
    #    answer = qa.run({"question": query, "chat_history": ConversationBufferMemory()})
        #chat_history = [(query, answer)] 
        #memory.save_context({"input": query}, {"output": answer})
     #   return answer