from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from Core.Config.ModelConfigurations import ModelConfigurations

from Core.Utils.AgentTools import get_manager_details


model = ModelConfigurations.get_hf_lang_chain_model_config()

featch_manager_detail_subagent = create_agent(
    model=model,
    tools=[get_manager_details],
    system_prompt="You are a helpful fantasy premier league assistant. you can use the tools fetch manager data from the FPL api."
)