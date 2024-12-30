from langchain_community.llms import Ollama
from load import load_csv
from agent import StudentAgent, CourseAgent, SupervisorAgent

llama3 = Ollama(model="stablelm2")

etudiants_db = load_csv("data/etudiants.csv")
cours_db = load_csv("data/cours.csv")

student_agent = StudentAgent("Agent Étudiant", llama3)
course_agent = CourseAgent("Agent Cours", llama3)


supervisor_agent = SupervisorAgent(etudiants_db, cours_db, student_agent, course_agent, llama3)

question = "Quel cours est enseigné par Mme Dupont ?"

response = supervisor_agent.route(question)
print(response)