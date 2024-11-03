from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.prompts import BasePromptTemplate
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import BaseConfig
from src.db.controllers import ctrl_operation


CUSTOM_PROMPT = (
    "Dado as seguintes informações sobre a minha sessão de usuário: {session_data}\n"
    "Gerar um relatório detalhado intitulado 'Operações com Vencimento Hoje' para a empresa {business_name}. \n"
    "Use como base o seguinte conjunto de dados {data_set}\n"
    "Incluir insights sobre a demografia dos clientes, métricas de engajamento e oportunidades de crescimento.\n"
    "O relatório deve incluir os seguintes elementos:\n"
    "1. Resumo executivo\n"
    "2. Análise detalhada\n"
    "3. Conclusão e recomendações\n\n"
    "Considere as melhores práticas para a apresentação de dados e insights de negócios."
    "O relatório so deve retornar os clientes que são meus. Se não tiver clientes no conjunto de dados então me retorne uma mensagem informativa da ausência dos dados"
)


class CurrentOperationsReportsGenerator:
    prompt: BasePromptTemplate = PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["business_name", "session_data", "data_set"],
    )
    config: BaseConfig

    def __load_data(self) -> list[dict]:
        operations = ctrl_operation.list(mode="all")
        return operations

    def __init__(self, session_data: dict):
        self.chain: Runnable = self.prompt | ChatGoogleGenerativeAI(
            model="gemini-1.5-flash"
        )

        self.config: BaseConfig = BaseConfig(
            business_name="Quark Investimentos",
            session_data=session_data,
            data_set=self.__load_data(),
        )

    def generate(self) -> str:
        formatted_prompt = dict(
            business_name=self.config.business_name,
            session_data=self.config.session_data,
            data_set=self.config.data_set,
        )
        ai_message: AIMessage = self.chain.invoke(formatted_prompt)
        response_data = ai_message.to_json().get("kwargs", {}).get("content", "")
        return response_data
