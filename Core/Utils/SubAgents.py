from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from Config.ModelConfigurations import ModelConfigurations

from Utils.AgentTools import get_manager_details


model = ModelConfigurations.get_gemini_lang_chain_model_config()

featch_manager_detail_subagent = create_agent(
    model=model,
    tools=[get_manager_details],
)