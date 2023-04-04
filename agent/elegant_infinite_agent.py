"""
This is a new implementation of the task tree concept, with a focus on elegance and simplicity.

The objective of this project remains the same: to create an LLM-powered autonomous agent that can do complex tasks like writing a short story from scratch, using only the user's input as a starting point.
"""

import os
import sys
import pickle
import time
from utils import openai_api_call
from task_class import Task
from action_interface import ActionInterface, RESPONSE_FORMATTING_INSTRUCTIONS
from task_tree_management import task_tree_management_action_set
from prompt import prompt_template
from sdf_writing_actions import writer_mode_action_set

# add path to SDF module, which is in ../SDF/
sys.path.append(os.path.join(os.path.dirname(__file__), "../SDF"))

from SDF import Document

class Agent:
    def __init__(self, task_description, action_sets, sdf_document=None, save_path="agent.pkl"):
        self.task_tree = Task(description=task_description)
        self.sdf_document = sdf_document # this is the document that the agent will be writing in writer mode
        self.action_interface = ActionInterface(action_sets, task_tree=self.task_tree, sdf_document=self.sdf_document)
        self.save_path = save_path

    def run(self, max_iterations=100, model_name="gpt-3.5-turbo", verbose=False):
        for _ in range(max_iterations):
            current_task = self.task_tree.find_next_task() # get the next task
            self.action_interface.task_tree = current_task # update the task tree used in the action interface
            if not current_task:
                print("There are no more tasks to complete.")
                break

            # construct the prompt
            prompt = prompt_template.format(
                local_task_tree=current_task.get_local_task_tree(),
                agent_action_log=self.action_interface.format_agent_action_log(),
                writer_mode_metadata=self.sdf_document.create_document_context(),
                available_actions=self.action_interface.get_available_actions_for_prompt(),
                response_formatting_instructions=RESPONSE_FORMATTING_INSTRUCTIONS,
            )

            # call the LLM
            response = openai_api_call(prompt, model_name=model_name, temperature=0.2, max_tokens=1000)
            if verbose: 
                print(f"Prompt sent to LLM:\n{prompt}\n")
                print(f"Raw response from LLM:\n{response}\n")
            
            # parse the response and perform the requested actions
            self.action_interface.parse_response_and_perform_actions(response)  

            # print the task tree after each iteration
            if verbose: self.task_tree.print_tree()

            # save the Agent object after each iteration
            with open(self.save_path, "wb") as f:
                pickle.dump(self, f)

            # add a short pause between iterations
            time.sleep(2)

task_description = "Write a long-form essay about the history of technology's impact on society."

human_notes = """
It should be written for a sophisticated audience.

Let's include lots of specific examples in this essay, so the reader feels like they're constantly learning new things. The specific examples should tie into the main thesis of the essay though.

This essay should be written in the style of a best-selling non-fiction author like Walter Isaacson or Malcolm Gladwell.

The essay should be about 10,000 words long. It should be broken up into 4-6 sections.
""".strip()

file_name = "technology_and_society.pkl"
model_name = "gpt-4" # "gpt-3.5-turbo"
pick_up_where_we_left_off = True

def main():
    if pick_up_where_we_left_off:
        with open(file_name, "rb") as f:
            agent = pickle.load(f)

        # Update the action interface to reflect changes made in the action sets
        agent.action_interface = ActionInterface(
            action_sets=[task_tree_management_action_set, writer_mode_action_set],
            task_tree=agent.task_tree,
            sdf_document=agent.sdf_document,
        )
    else:
        # Create an agent with an initial task description
        agent = Agent(
            task_description=task_description,
            action_sets=[task_tree_management_action_set, writer_mode_action_set],
            sdf_document=Document(title="Untitled", human_notes=human_notes, section_type="Section", model_name=model_name),
            save_path=file_name,
        )

    # Run the agent for a specified number of iterations
    agent.run(max_iterations=100, model_name=model_name, verbose=True)

    # Print the final task tree
    print("\nFinal Task Tree:")
    agent.task_tree.print_tree()

    # Print the final SDF document
    print("\nFinal SDF Document:")
    agent.sdf_document.display()


if __name__ == "__main__":
    main()