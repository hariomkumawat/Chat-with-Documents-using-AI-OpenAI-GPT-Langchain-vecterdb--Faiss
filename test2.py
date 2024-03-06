
import json
import openai
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# from langchain_faiss import Document

from openai import OpenAI
client = OpenAI(api_key="Your_api_Key")
key='Your_api_Key'
# openai.api_key = key
embeddings=OpenAIEmbeddings(api_key=key)




db = FAISS.load_local("faiss_index",embeddings)


########################################
# # query=input('User: ')
# query=' In FY 2023, your company delivered revenue is '
# docs = db.similarity_search(query)

# retriever = db.as_retriever()
# docs = retriever.invoke(query)
# # print(docs[2].page_content)
# doc_text = docs[0].page_content 
# # print(doc_text)
# print("$$$$$$$$")
# print(type(docs))
# json_data = {


# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": doc_text},
#     {"role": "user", "content": query},

#   ]
# )


# generated_text = completion.choices[0].message.content

# # Process the generated text as needed
# print("Generated text:", generated_text)

#########################################


while input != "quit()":
    query = input("User:")
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
    
    print("\n"+ reply + "\n")
print("your new assistant is ready!")
