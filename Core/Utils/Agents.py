from Utils.SubAgents import featch_manager_detail_subagent
from langchain.tools import tool
from langchain.messages import HumanMessage


@tool
def call_manager_detail_subagent(manager_id : int) -> str:
    """call featch_manager_detail_subagent in order to featch the manager details from FPL api end point"""
    response = featch_manager_detail_subagent.invoke({
        "messages" : [HumanMessage(content=f"The FPL manager id is {manager_id}")]
    })