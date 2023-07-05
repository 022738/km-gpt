from langchain.llms import VertexAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationChain
#from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
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
#doc_chain = load_qa_with_sources_chain(llm, chain_type="stuff")
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
qa_chain = load_qa_with_sources_chain(llm, chain_type="stuff")
qa = ConversationalRetrievalChain( retriever=retriever,question_generator=question_generator,memory=memory, combine_docs_chain=qa_chain, return_source_documents=True)

while True:
    query = input("> ")
    if query =="clear memory":
        memory.clear()
        answer = "I've wiped our conversation"
    else:
        try:

            #answer = qa({"question": query,"chat_history": ConversationBufferMemory()})
            answer = qa({"question": query})
        except Exception as err:
            print (err)
            print (err.message)
#    print(answer['answer'])
    print("lenght of array %i", len(answer['source_documents']))
    if len(answer['source_documents'])>0:    
        formattedanswer = answer['answer'] + "\nTitle:  " +  answer['source_documents'][0].metadata['title'] + "\nFile url: " +  answer['source_documents'][0].metadata['source'] 
        print(formattedanswer)
    else:
        print(answer['answer'])
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
