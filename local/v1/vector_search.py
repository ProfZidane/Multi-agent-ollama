from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class VectorSearch:
    def __init__(self, etudiants_db, cours_db):
        self.etudiants_db = etudiants_db
        self.cours_db = cours_db
        self.vectorizer = TfidfVectorizer()
        self.documents = self.etudiants_db + self.cours_db        
        self.document_vectors = self.vectorizer.fit_transform([json.dumps(doc) for doc in self.documents])
        

    def search(self, query):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors)
        top_indices = similarities.argsort()[0][-5:]  # Récupère les 5 documents les plus pertinents
        relevant_docs = [self.documents[i] for i in top_indices]
        return relevant_docs
