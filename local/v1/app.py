from langchain_community.llms import Ollama
from agent import StudentAgent, CourseAgent, SupervisorAgent
from load import load_csv

llama3 = Ollama(model="stablelm2")

etudiants_db = load_csv("data/etudiants.csv")
cours_db = load_csv("data/cours.csv")

# Initialisation des agents
student_agent = StudentAgent("Agent Étudiant", llama3)
course_agent = CourseAgent("Agent Cours", llama3)


# Création de l'agent superviseur
supervisor_agent = SupervisorAgent(student_agent, course_agent, llama3)

question = "Quel cours enseigne Mme Dupont ?"
response = supervisor_agent.route(question, etudiants_db=etudiants_db, cours_db=cours_db)
print(response)