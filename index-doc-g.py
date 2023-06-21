import os.path
# from langchain.chat_models import ChatOpenAI
from langchain.llms import VertexAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import Chroma
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#changed persist directory to run google in paralell
persist_directory = 'gvectordb'
SAMPLE_SPREADSHEET_ID = '1Ctnp3t1mSly30ukrz9rYcEp5asA-PzrN11YvpZkg18k'
SAMPLE_RANGE_NAME = 'Documents!A2:A22'
logging.basicConfig(filename='output.txt', level=logging.INFO, format='')
embeddings = VertexAIEmbeddings()

if os.path.exists('/home/matt_cheung/.credentials/keys.json'):
        
    creds = service_account.Credentials.from_service_account_file('/home/matt_cheung/.credentials/keys.json', scopes=scopes)
#get the document ids to train the model
    try:
    
        service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        docs_to_index =[] 
        print('Received these documents to index')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s' % (row[0]))
            docs_to_index.append(row[0])
    
    except HttpError as err:
        print(err)
#get the contents of the documents
loader = GoogleDriveLoader(
   document_ids=docs_to_index
   )
docs = loader.load()
#split the docs into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"]
     )
texts = text_splitter.split_documents(docs)

embeddings = VertexAIEmbeddings()
db =Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory) 

print("completed loading", db)


logging.info('Completed build')
