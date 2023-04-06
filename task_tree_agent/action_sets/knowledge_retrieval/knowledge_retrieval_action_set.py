from agent.action_interface import Action, ActionSet

def superpowered_knowledge_base_search(query):
    """
    
    """

def google_search(query):
    """
    Use this function to search Google and view the first ten results.
    Arguments:
      - query: The query to search Google with.
    """
    import webbrowser
    webbrowser.open("https://www.google.com/search?q=" + query)

google_search_action = Action(name="google_search(query)", 
                              when_to_use="Use this function to search Google.", 
                              arguments="Arguments:\n  - query: The query to search Google with.", 
                              action_function=google_search,
                              )

knowledge_retrieval_actions_list = [
    google_search_action,
]

knowledge_retrieval_action_set = ActionSet(action_list=knowledge_retrieval_actions_list, action_set_name="knowledge_retrieval_action_set", action_set_object=None)