import os
import sys
from superpowered import get_knowledge_base

# add task_tree_agent to the path. It's not installed as a package, so we need to add it to the path manually.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "task_tree_agent"))

from agent.action_interface import Action, ActionSet

class SuperpoweredKnowledgeBase:
    def __init__(self, kb_title):
        self.kb_title = kb_title
        self.retriever_top_k = 100
        self.reranker_top_k = 5

    def query(self, query):
        # make an API call to the Superpowered knowledge base using the SDK
        kb = get_knowledge_base(self.kb_title)
        return kb.query(query, retriever_top_k=self.retriever_top_k, reranker_top_k=self.reranker_top_k)


def superpowered_kb_search(sp_kb_object, query):
    return sp_kb_object.query(query)

superpowered_kb_search_action = Action(
    name="superpowered_kb_search(query: str)",
    when_to_use="Use this when you want to search a knowledge base",
    arguments="Arguments:\n - query (str): The query to search the knowledge base with."
    action_function=superpowered_kb_search,
)

knowledge_retrieval_actions_list = [
    superpowered_kb_search_action,
]

knowledge_retrieval_action_set = ActionSet(action_list=knowledge_retrieval_actions_list, action_set_name="knowledge_retrieval_action_set", action_set_object=None)