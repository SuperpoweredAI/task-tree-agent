import os
import sys

# add task_tree_agent to the path. It's not installed as a package, so we need to add it to the path manually.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "task_tree_agent"))

import pickle
from agent.agent_class import Agent
from action_sets.task_tree.task_tree_management import task_tree_management_action_set
from action_sets.long_form_writing.SDF import Document
from action_sets.long_form_writing.writing_action_set import writing_action_set
from action_sets.knowledge_retrieval.knowledge_retrieval_action_set import knowledge_retrieval_action_set, SuperpoweredKnowledgeBase

task_description = "Do a legal analysis of the following business idea: A company that uses AI to identify and analyze potential investments for clients. Assume the company is registered as an investment adviser with the SEC. Once you have completed the analysis, write a detailed report for the CEO of the company."

human_notes = """
Provide a detailed analysis of the legal risks associated with this business idea. The analysis should be written for the CEO of the business. Be very detailed and thorough. You should also include a summary of the legal risks at the beginning of the report.

You have access to the full text of the Investment Advisers Act of 1940 via a Superpowered AI knowledge base that you can query. Be sure to use it.
""".strip()

constitution = """
1. Never do anything that could cause harm to humans.
2. Pay attention to human guidance and do not disobey it.
3. Always try your best to be as helpful as possible.
""".strip()

file_name = "legal_analysis_of_business_idea.pkl" # this is the file that the agent will save to and load from
model_name = "gpt-4" # "gpt-3.5-turbo"

# add necessary objects to the action sets
writing_action_set.update_action_set_object(Document(title="Final Legal Analysis", human_notes=human_notes, section_type="Section", model_name=model_name))
knowledge_retrieval_action_set.update_action_set_object(SuperpoweredKnowledgeBase(kb_title="Investment Advisers Act of 1940"))

pick_up_where_we_left_off = True

def main():
    if pick_up_where_we_left_off:
        # Load the agent from a pickle file
        with open(file_name, "rb") as f:
            agent = pickle.load(f)
    else:
        # Create an agent with a task description and action sets
        agent = Agent(
            task_description=task_description,
            action_sets=[task_tree_management_action_set, writing_action_set, knowledge_retrieval_action_set],
            constitution=constitution,
            save_path=file_name,
        )

    # Run the agent for a specified number of iterations
    agent.run(max_iterations=3, model_name=model_name, verbose=True)

    # Print the final task tree
    print("\nFinal Task Tree:")
    agent.task_tree.print_tree()

    # Print the final SDF document
    print("\nFinal SDF Document:")
    writing_action_set.action_set_object.display()


if __name__ == "__main__":
    main()