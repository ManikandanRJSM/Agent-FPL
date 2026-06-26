from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from Core.Config.ModelConfigurations import ModelConfigurations

from Core.Utils.AgentTools import get_manager_details, get_player_suggestion


model = ModelConfigurations.get_hf_lang_chain_model_config()

featch_manager_detail_subagent = create_agent(
    model=model,
    tools=[get_manager_details],
    system_prompt="You are a helpful fantasy premier league assistant. you can use the tools fetch manager data from the FPL api."
)


player_suggestion_subagent = create_agent(
    model=model,
    tools=[get_player_suggestion],
    system_prompt="""
    You are a helpful fantasy premier league assistant. you can use the tools to fetch all players data which is stored in the local.
    In fpl a user can have 2 goalkeeprs, 5 defenders, 5 midfielders, 3 strikers this user currently satisfies all numbers inclusion of this player.
    you have to suggest a best player to transfer based on this constraints for particular position you can see details for selected player from the json and manager transfer balance.
    Be concise"""
)