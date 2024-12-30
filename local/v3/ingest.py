from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import csv
import os
from langchain_community.document_loaders import CSVLoader, TextLoader
from uuid import uuid4
from langchain.schema import Document  

documents = []

def load_csv(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def load_all_files():
    for root, dirs, files in os.walk("data"):
        for file in files:            
            file_path = os.path.join(root, file)
            if file.endswith(".csv"):
                documents.extend(CSVLoader(file_path).load())
            elif file.endswith(".txt"):
                documents.extend(TextLoader(file_path).load())
    


def ingestion():
    # Charger les fichiers
    load_all_files()
        
    if not documents:
        print("Aucun document n'a été chargé. Vérifiez le dossier 'data'.")
        return

    # Diviser les documents en chunks
    print("Début de la découpe des documents en chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)

    print(f"Nombre de chunks générés : {len(chunks)}")
    if chunks:
        print("Exemple de chunk :", chunks[0])

    formatted_chunks = [
        Document(page_content=chunk.page_content, metadata=chunk.metadata)
        for chunk in chunks
    ]
    print("Exemple de chunk formaté :", formatted_chunks[0])

    # Créer les embeddings
    print("Initialisation des embeddings FastEmbed...")
    embedding = FastEmbedEmbeddings()

    # Initialiser Chroma
    persist_directory = "./embeddings/sql_chroma_db"
    print("Création du vector store Chroma...")
    vector_store = Chroma(
        collection_name="documents",
        persist_directory=persist_directory,
        embedding_function=embedding,
    )

    
    batch_size = 5  
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        uuids = [str(uuid4()) for _ in range(len(batch))]
        try:
            print(f"Ajout des chunks {i}-{i+batch_size}...")
            vector_store.add_documents(batch, ids=uuids)
            print(f"Chunks {i}-{i+batch_size} ajoutés.")
        except Exception as e:
            print(f"Erreur lors de l'ajout des chunks {i}-{i+batch_size}: {e}")

    
    
    