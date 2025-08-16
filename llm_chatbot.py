class Chatbot:
    def __init__(self, ia_engine):
        self.ia_engine = ia_engine

    def get_response(self, user_question, context_data):
        """
        Simula a resposta de um LLM com base na pergunta do usuário
        e nos dados de contexto da lavoura.
        
        Em uma implementação real, a pergunta seria enviada a uma API de LLM.
        """
        user_question = user_question.lower()
        
        if "irrigação" in user_question and "hoje" in user_question:
            plan = self.ia_engine.generate_irrigation_plan(context_data['sensor'], context_data['weather'])
            return f"Com base nos dados atuais: {plan}"
        
        elif "produtividade" in user_question:
            prediction = self.ia_engine.predict_productivity(context_data['historical'])
            return f"A previsão de produtividade para a próxima safra é de {prediction}."
            
        elif "saúde da lavoura" in user_question or "ndvi" in user_question:
            ndvi = self.ia_engine.get_last_ndvi(context_data['satellite'])
            return f"O valor médio de NDVI na sua lavoura é de {ndvi:.4f}, indicando uma saúde geral boa."

        else:
            return "Desculpe, não entendi a sua pergunta. Por favor, seja mais específico sobre o manejo, produtividade ou saúde da lavoura."
