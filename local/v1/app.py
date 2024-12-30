from langchain_community.llms import Ollama
from agent import StudentAgent, CourseAgent, SupervisorAgent
from load import load_csv
from vector_search import VectorSearch

llama3 = Ollama(model="stablelm2")

etudiants_db = load_csv("data/etudiants.csv")
cours_db = load_csv("data/cours.csv")

# Initialisation des agents
student_agent = StudentAgent("Agent Étudiant", llama3)
course_agent = CourseAgent("Agent Cours", llama3)


# Création de l'agent superviseur
supervisor_agent = SupervisorAgent(student_agent, course_agent, llama3)
vector_search = VectorSearch(etudiants_db, cours_db)


question = "Quel cours enseigne Mme Dupont ?"

# Récupération des documents pertinents
relevant_docs = vector_search.search(question)

response = supervisor_agent.route(question, relevant_docs=relevant_docs)
print(response)