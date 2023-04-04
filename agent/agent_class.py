import os
import sys
import pickle
from utils import openai_api_call
from prompt import prompt_template

# add paths to action sets
sys.path.append(os.path.join(os.path.dirname(__file__), "../action_sets/task_tree"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../action_sets/long_form_writing"))

from task_class import Task
from action_interface import ActionInterface, RESPONSE_FORMATTING_INSTRUCTIONS

class Agent:
    def __init__(self, task_description, action_sets, save_path="agent.pkl"):
        self.task_tree = Task(description=task_description)
        self.action_interface = ActionInterface(action_sets)
        self.save_path = save_path

    def run(self, max_iterations=100, model_name="gpt-4", verbose=False):
        for _ in range(max_iterations):
            current_task = self.task_tree.find_next_task() # get the next task
            self.action_interface.update_action_set_object("task_tree_management_action_set", current_task) # update the task tree used in the action interface to the current task
            if not current_task:
                print("There are no more tasks to complete.")
                break

            # construct the prompt
            prompt = prompt_template.format(
                local_task_tree=current_task.get_local_task_tree(),
                agent_action_log=self.action_interface.format_agent_action_log(),
                action_set_prompt_context=self.action_interface.get_action_set_prompt_context(),
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