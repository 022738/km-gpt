import os.path
# from langchain.chat_models import ChatOpenAI
from langchain.llms import VertexAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.document_loaders import UnstructuredFileIOLoader
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

scopes = ['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/spreadsheets.readonly']
#changed persist directory to run google in paralell
persist_directory = 'gvectordb'
SAMPLE_SPREADSHEET_ID = '1Ctnp3t1mSly30ukrz9rYcEp5asA-PzrN11YvpZkg18k'
SAMPLE_RANGE_NAME = 'Documents!A2:A122'
logging.basicConfig(filename='output.txt', level=logging.INFO, format='')
embeddings = VertexAIEmbeddings()
docs_to_index=[]
if os.path.exists('/home/matt_cheung/.credentials/keys.json'):
    creds = service_account.Credentials.from_service_account_file('/home/matt_cheung/.credentials/keys.json', scopes=scopes)
    try:
        #get the document ids to train the model
        service = build('sheets', 'v4', credentials=creds)
        driveservice = build("drive", "v3", credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                     range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        print('Received these documents to index')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # Check that service agent can access
            try:
                file = driveservice.files().get(fileId=row[0], supportsAllDrives=True).execute()
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s' % (row[0]))
                docs_to_index.append(row[0])                
            except HttpError as e:
                if e.resp.status == 404:
                    print("File not found: {}".format(row[0]) )
                    logging.error("File not found: {}".format(row[0]))
                else:
                    print("An error occurred: {}".format(e))
                    logging.error("An error occured:{}".format(e))
            

    
    #get the contents of the documents
        loader = GoogleDriveLoader(document_ids=docs_to_index, file_loader_cls=UnstructuredFileIOLoader,
    file_loader_kwargs={"mode": "elements"})
        docs = loader.load()
        #split the docs into chunks
        text_splitter = RecursiveCharacterTextSplitter(
                  chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"] )
        texts = text_splitter.split_documents(docs)

        embeddings = VertexAIEmbeddings()
        db =Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory) 

    except HttpError as err:
        print(err)

    print("completed loading", db)
else:
    print("Couldn't initialise")

logging.info('Completed build')
