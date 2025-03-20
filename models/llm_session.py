from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from config import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
from models.job_search_model import JobSearchModel
from models.job_details_model import JobDetailModel


class LLMSession:
    """A class to manage Language Learning Model (LLM) sessions across different providers.

    This class provides a unified interface to interact with various LLM providers
    including OpenAI, Anthropic, Ollama, and Google. It handles the initialization
    of the appropriate LLM client based on the specified provider and model.

    Attributes:
        provider (str): The LLM provider name (openai, anthropic, ollama, or google)
        model (str): The specific model name to use with the provider
        llm: The initialized LLM client instance
        structured_llm_js: The LLM client configured for structured output - JobSearchModel
        structured_llm_jd: The LLM client configured for structured output - JobDetailModel
    """

    def __init__(self, provider=LLM_PROVIDER, model=LLM_MODEL):
        """Initialize a new LLM session.

        Args:
            provider (str, optional): The LLM provider to use. Defaults to value from global config.
            model (str, optional): The model name to use. Defaults to value from global config.

        Raises:
            Exception: If an invalid provider is specified.
        """
        self.provider = provider
        self.model = model

        model_providers = {
            "openai": lambda: ChatOpenAI(model=self.model, openai_api_key=OPENAI_API_KEY),
            "anthropic": lambda: ChatAnthropic(model=self.model, anthropic_api_key=ANTHROPIC_API_KEY),
            "ollama": lambda: ChatOllama(model=self.model),
            "google": lambda: ChatGoogleGenerativeAI(model=self.model, google_api_key=GOOGLE_API_KEY),
        }

        if self.provider not in ["openai", "ollama", "anthropic", "google"]:
            raise Exception(f"Invalid LLM provider: {self.provider}")

        self.llm = model_providers[self.provider]()

        if self.provider == "google":
            self.structured_llm_js = self.llm.with_structured_output(JobSearchModel)
        else:
            self.structured_llm_js = self.llm.with_structured_output(JobSearchModel, method="json_mode")

        if self.provider == "google":
            self.structured_llm_jd = self.llm.with_structured_output(JobDetailModel)
        else:
            self.structured_llm_jd = self.llm.with_structured_output(JobDetailModel, method="json_mode")

    def invoke(self, message):
        """Send a message to the LLM and get a structured response.

        Args:
            message (list): The input message or prompt to send to the LLM: [SystemMessage, HumanMessage].

        Returns:
            list: A structured response containing the query and explanation.
        """
        return self.llm.invoke(message)
    
    def search_job(self, message):
        """Send a message to the LLM and get a structured response.

        Args:
            message (list): The input message or prompt to send to the LLM: [SystemMessage, HumanMessage].

        Returns:
            JobSearchModel: A structured response.
        """
        return self.structured_llm_js.invoke(message)
    
    def detail_job(self, message):
        """Send a message to the LLM and get a structured response.

        Args:
            message (list): The input message or prompt to send to the LLM: [SystemMessage, HumanMessage].

        Returns:
            JobDetailModel: A structured response.
        """
        return self.structured_llm_jd.invoke(message)