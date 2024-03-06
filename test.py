
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS




## Lets Read the document
def read_doc (directory):
    file_loader=PyPDFDirectoryLoader (directory)
    documents=file_loader.load()
    return documents

doc=read_doc('documents/')
# print(doc)



## Divide the docs into chunks
# https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacte
def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc=text_splitter.split_documents (docs)
    return doc

documents=chunk_data(docs=doc)
# print(documents[0])
print(len(documents))

###########################################


# Embedding Technique Of OPENAI

embeddings=OpenAIEmbeddings (api_key='Your_api_Key')
# print(embeddings)


vectors=embeddings.embed_query('what is Flask ')
print(vectors)
print(len(vectors))


db = FAISS.from_documents(documents, embeddings)
print(db)

db.save_local("faiss_index")



# query = "what is Flask"
# docs = db.similarity_search(query)
# # docs_and_scores = db.similarity_search_with_score(query)
# # print(docs[0].page_content)
# # print(docs_and_scores[0])

# retriever = db.as_retriever()
# docs = retriever.invoke(query)
# print(docs)



