from ingest import ingestion
from retrieval import retrieval
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from huggin_access import login_huggingface

# N'oublions pas d'ingérer les documents avant de lancer le RAG
# ingestion()

login_huggingface()

prompt = PromptTemplate.from_template(
        """
        <s> [Instructions] You are a friendly assistant. Answer the question based only on the following context. 
        If you don't know the answer, then reply, No Context availabel for this question {input}. [/Instructions] </s> 
        [Instructions] Question: {input} 
        Context: {context} 
        Answer: [/Instructions]
        """
    )


model = ChatOllama(model="stablelm2")

question = "Donne-moi les informations de l'étudiant Jean Dupont."

retrieved_docs = retrieval(query=question)

context = "\n".join([doc.page_content for doc in retrieved_docs])

prompt_with_context = prompt.format(input=question, context=context)

response = model.invoke(prompt_with_context)

print(response.content)
