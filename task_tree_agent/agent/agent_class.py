import pickle
import os
import sys

# add task_tree_agent to the path. It's not installed as a package, so we need to add it to the path manually. It's in ../../task_tree_agent
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "task_tree_agent"))

from agent.utils import openai_api_call
from agent.prompt import prompt_template

from action_sets.task_tree.task_class import Task
from agent.action_interface import ActionInterface, RESPONSE_FORMATTING_INSTRUCTIONS

class Agent:
    def __init__(self, task_description, action_sets, constitution="", save_path="agent.pkl"):
        self.task_tree = Task(description=task_description)
        self.action_interface = ActionInterface(action_sets)
        self.save_path = save_path
        self.human_input_list = []
        self.constitution = constitution

    def format_human_input_list(self, max_messages=10):
        return "\n".join([" - " + message for message in self.human_input_list[-max_messages:]])

    def run(self, max_iterations=10, model_name="gpt-4", verbose=False):
        for _ in range(max_iterations):
            current_task = self.task_tree.find_next_task() # get the next task
            self.action_interface.update_action_set_object("task_tree_management_action_set", current_task) # update the task tree used in the action interface to the current task
            if not current_task:
                print("There are no more tasks to complete.")
                break

            # ask for human input
            human_input = input("Do you have any guidance for me? Press enter to skip.\n\nUSER INPUT: ")
            if not human_input:
                human_input_for_prompt = "None"
            else:
                human_input_for_prompt = human_input

            # construct the prompt
            prompt = prompt_template.format(
                local_task_tree=current_task.get_local_task_tree(),
                constitution=self.constitution,
                agent_action_log=self.action_interface.format_agent_action_log(),
                action_set_prompt_context=self.action_interface.get_action_set_prompt_context(),
                human_input_list=self.format_human_input_list(),
                current_human_input=human_input_for_prompt,
                available_actions=self.action_interface.get_available_actions_for_prompt(),
                response_formatting_instructions=RESPONSE_FORMATTING_INSTRUCTIONS,
            )

            if verbose: print(f"Prompt sent to LLM:\n{prompt}\n")

            # call the LLM
            response = openai_api_call(prompt, model_name=model_name, temperature=0.2, max_tokens=1000)
                
            formatted_response = self.action_interface.format_response(response)
            print(f"\nAGENT THOUGHTS: {formatted_response}\n")
            
            # parse the response and perform the requested actions
            self.action_interface.parse_response_and_perform_actions(response)  

            # print the task tree after each iteration
            if verbose: self.task_tree.print_tree()

            # we want to save the human input for later
            if human_input:
                self.human_input_list.append(human_input.strip())

            # save the Agent object after each iteration
            with open(self.save_path, "wb") as f:
                pickle.dump(self, f)