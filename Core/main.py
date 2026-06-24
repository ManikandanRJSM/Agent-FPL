import sys
import os

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to the front of sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from Utils.load_env import get_env_variables

# os.environ['HUGGINGFACEHUB_API_TOKEN'] = get_env_variables()['HF_TOKEN']
os.environ['GOOGLE_API_KEY'] = get_env_variables()['GOOGLE_API_KEY']

from Utils.Agents import call_manager_detail_subagent
from Config.ModelConfigurations import ModelConfigurations
from langchain.messages import HumanMessage


from langchain.agents import create_agent

model = ModelConfigurations.get_gemini_lang_chain_model_config()

"You are a helpful fantasy premier league assistant. you provide transfer suggestion, squad builder. you can use the tools featch data from the FPL api."

agent = create_agent(
    model=model,
    tools=[call_manager_detail_subagent],
    system_prompt="You are a helpful fantasy premier league assistant. you provide transfer suggestion, squad builder. you can use the tools featch data from the FPL api."
)

response = agent.invoke({
        "messages" : [HumanMessage(content=f"Get the details for FPL manager 5125930")]
    })

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )
print(response["messages"][-1].content_blocks)