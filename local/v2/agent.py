from vector_search import VectorSearch


class Agent:
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm

    def query(self, question, relevant_docs):
        raise NotImplementedError("Chaque agent doit implémenter la méthode query.")
     


class StudentAgent(Agent):
    def query(self, question, vector_search):

        # Récupérer les documents pertinents
        relevant_docs = vector_search.search(question)
        print(relevant_docs)
        # Utiliser le LLM pour répondre directement à la question
        prompt = f"""
        NE DONNE PAS PLUS D'INFORMATIONS QUE NÉCESSAIRE. REPONDS SEULEMENT À LA QUESTION :
        EXEMPLE DE QUESTION : "Quel est le prénom de l'étudiant avec l'ID 123 ?"
        EXEMPLE DE REPONSE : "Le prénom de l'étudiant avec l'ID 123 est Jean."

        Vous êtes un assistant étudiant. Répondez à cette question en utilisant les données suivantes sur les étudiants :
        {relevant_docs}
        
        Question : {question}
        """
        response = self.llm(prompt)
        return response
    

class CourseAgent(Agent):
    def query(self, question, vector_search):
        # Récupérer les documents pertinents
        relevant_docs = vector_search.search(question)
        print(relevant_docs)
        # Utiliser le LLM pour répondre directement à la question
        prompt = f"""
        NE DONNE PAS PLUS D'INFORMATIONS QUE NÉCESSAIRE. REPONDS SEULEMENT À LA QUESTION :
        EXEMPLE DE QUESTION : "Quelles sont les matières en Physique ?"
        EXEMPLE DE REPONSE : "Les matières en Physique sont Mécanique, Thermodynamique, et Électricité."
        
        Vous êtes un assistant académique. Répondez à cette question en utilisant les données suivantes sur les cours :
        {relevant_docs}
        
        Question : {question}
        """
        response = self.llm(prompt)
        return response

    


# Agent superviseur
class SupervisorAgent:
    def __init__(self, etudiants_db, cours_db, student_agent, course_agent, llm):
        self.student_agent = student_agent
        self.course_agent = course_agent
        self.llm = llm
        self.etudiants_db = etudiants_db
        self.cours_db = cours_db

    def route(self, question):
        # Utiliser le LLM pour déterminer l'agent approprié
        prompt = f"""
        Vous êtes un superviseur pour un système multi-agent. Analysez cette question et identifiez si elle concerne un étudiant ou un cours :
        Question : {question}
        Répondez par "étudiant" ou "cours". Si vous n'êtes pas sûr, répondez "inconnu".
        """

        response = self.llm(prompt).strip().lower()

        if "étudiant" in response:
            print("Route 1")
            vector_search = VectorSearch(self.etudiants_db)
            return self.student_agent.query(question, vector_search)
        elif "cours" in response:
            print("Route 2")
            vector_search = VectorSearch(self.cours_db)
            return self.course_agent.query(question, vector_search)
        else:
            return "Je ne sais pas vers quel agent diriger votre question."



