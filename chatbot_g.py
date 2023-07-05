from langchain.llms import VertexAI
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT

persist_directory = 'gvectordb'
#folder_id = "1HkHnvAYonewerZRWD0vDNf5HemeXbDjg"
embeddings = VertexAIEmbeddings()
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer')
print("I do think I have a db", db)
retriever = db.as_retriever()

llm = VertexAI(temperature=0)
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
qa_chain = load_qa_with_sources_chain(llm, chain_type="stuff")
qa = ConversationalRetrievalChain( retriever=retriever,question_generator=question_generator,memory=memory, combine_docs_chain=qa_chain, return_source_documents=True)

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
                answer = qa({"question": query})
            except Exception as err:
                answer = "An error occurred. Context: "+err.message
        if len(answer['source_documents'])>0:    
            answer = answer['answer'] + "\nTitle: " +  answer['source_documents'][0].metadata['title'] + "\nFile url: " +  answer['source_documents'][0].metadata['source'] 
        return answer
