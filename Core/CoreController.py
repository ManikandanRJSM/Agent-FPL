import sys
import os

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to the front of sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from Utils.load_env import get_env_variables

os.environ['HUGGINGFACEHUB_API_TOKEN'] = get_env_variables()['HF_TOKEN']

# from Utils.Agents import call_manager_detail_subagent
from Core.Config.ModelConfigurations import ModelConfigurations
from langchain.messages import HumanMessage
from Core.Utils.SubAgents import featch_manager_detail_subagent


from langchain.agents import create_agent


class Agents():
    def __init__(self, **kwargs):
        self.model = ModelConfigurations.get_hf_lang_chain_model_config()

    def featchManagerAgent(self, manager_id : int) -> str:

        "You are a helpful fantasy premier league assistant. you provide transfer suggestion, squad builder. you can use the tools fetch data from the FPL api."

        response = featch_manager_detail_subagent.invoke({
            "messages" : [HumanMessage(content=f"Get the details for FPL manager {manager_id}")]
        })

        for msg in response["messages"]:
            print(type(msg).__name__, "->", msg.content)

        # agent = create_agent(
        #     model=self.model,
        #     tools=[call_manager_detail_subagent],
        #     system_prompt="You are a helpful fantasy premier league assistant. you provide transfer suggestion, squad builder. you can use the tools fetch data from the FPL api."
        # )

        # response = agent.invoke({
        #         "messages" : [HumanMessage(content=f"Get the details for FPL manager 5125930")]
        # })
        return response["messages"][-1].content_blocks