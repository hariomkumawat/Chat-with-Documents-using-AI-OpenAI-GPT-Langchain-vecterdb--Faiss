# from distutils.log import debug 
from fileinput import filename 
from flask import render_template,request,Flask,redirect


from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS




app = Flask(__name__)
 

@app.route('/') 
def main(): 
	return render_template("index.html") 


embeddings=OpenAIEmbeddings (api_key='api_key')


def read_doc (directory):
    file_loader=PyPDFDirectoryLoader (directory)
    documents=file_loader.load()
    return documents

def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc=text_splitter.split_documents (docs)
    return doc

@app.route('/success', methods = ["GET",'POST']) 
def success(): 
	if request.method == 'POST': 
            f = request.files['file'] 
            f.save('uploads/' + f.filename) 
            doc=read_doc('uploads/')
            documents=chunk_data(docs=doc)
            db = FAISS.from_documents(documents, embeddings)
            # print(db)

            db.save_local("faiss_index1")
            return redirect("/") 
      

########################################
import json
import openai
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
# from langchain_faiss import Document
from openai import OpenAI
client = OpenAI(api_key="api_key")
key='api_key'
# openai.api_key = key
embeddings=OpenAIEmbeddings(api_key=key)



db = FAISS.load_local("faiss_index",embeddings)
@app.route('/chat', methods = ['GET','POST']) 
def chat():
        if request.method == 'POST':
        
                query =  request.form['message']
                docs = db.similarity_search(query)

                retriever = db.as_retriever()
                docs = retriever.invoke(query)
                # print(docs[2].page_content)
                doc_text = docs[0].page_content 
                completion = client.chat.completions.create(model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": doc_text},
                {"role": "user", "content": query},

            ]
            )
                reply = completion.choices[0].message.content
                return render_template('chat.html', response=reply,query=query)    
            #     print("\n"+ reply + "\n")
            # print("your new assistant is ready!")
        return render_template('chat.html')

if __name__ == '__main__': 
	app.run(debug=True)
