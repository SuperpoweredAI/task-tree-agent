import json

class Action:
    def __init__(self, name: str, when_to_use: str, arguments: str, action_function, action_set_name: str=None, action_set_object=None):
        self.name = name # function name, in string format, with arguments and their types - MUST identically match the function signature (except for arguments)
        self.when_to_use = when_to_use # description of when to use the action
        self.arguments = arguments # description of the arguments for the action, as a string
        self.action_function = action_function # callable function
        self.action_set_name = action_set_name # name of the action set that contains this action
        self.action_set_object = action_set_object # optional object used by the action set

    def perform(self, *args, **kwargs):
        return self.action_function(*args, **kwargs)
    

class ActionSet:
    def __init__(self, action_list: list, action_set_name: str, action_set_object):
        self.action_list = action_list # list of Action objects
        self.action_set_name = action_set_name # name of the action set
        self.action_set_object = action_set_object

        # add the action set name and object to each action
        for action in self.action_list:
            action.action_set_name = self.action_set_name
            action.action_set_object = self.action_set_object

    def update_action_set_object(self, action_set_object):
        self.action_set_object = action_set_object
        for action in self.action_list:
            action.action_set_object = action_set_object
    
    def format_prompt_context(self):
        # look for a function called "format_prompt_context" in the action set object
        if hasattr(self.action_set_object, "format_prompt_context"):
            return self.action_set_object.format_prompt_context()
        else:
            return None

    
class ActionInterface:
    """
    Contains functions for working with action sets and performing actions.
    """
    def __init__(self, action_set_list):
        self.action_set_list = action_set_list # save our list of ActionSet objects
        self.action_list = get_action_list(action_set_list) # create list of all Action objects
        self.agent_action_log = []

    def get_action(self, action_name):
        for action in self.action_list:
            function_name = action.name.split("(")[0]
            if function_name == action_name:
                return action
        return None
    
    def get_action_set(self, action_set_name):
        for action_set in self.action_set_list:
            if action_set.action_set_name == action_set_name:
                return action_set
        return None
    
    def get_action_set_prompt_context(self):
        """
        add additional context associated with each action set
        """
        context_str = ""
        for action_set in self.action_set_list:
            prompt_context = action_set.format_prompt_context()
            if prompt_context:
                context_str += prompt_context + "\n\n"
        return context_str.strip()
    
    def get_available_actions_for_prompt(self):
        available_actions_str = ""
        for action in self.action_list:
            available_actions_str += f"{action.name}\nUsage: {action.when_to_use}\n{action.arguments}\n\n"
        return available_actions_str.strip()
    
    def update_action_set_object(self, action_set_name, action_set_object):
        for action in self.action_list:
            if action.action_set_name == action_set_name:
                action.action_set_object = action_set_object

        for action_set in self.action_set_list:
            if action_set.action_set_name == action_set_name:
                action_set.action_set_object = action_set_object
    
    def parse_response_and_perform_actions(self, response):
        """
        This function relies on the LLM being prompted to respond with a JSON string containing a list of action dictionaries.
        """
        # Extract the action JSON string from the response, starting with the first open square bracket
        actions_json_str = response.strip()[response.strip().find("["):]

        if not actions_json_str:
            error_message = "Warning: Empty response from LLM."
            print(error_message)
            self.agent_action_log.append(self.format_error_message(error_message, response)) # Add the error message to the agent's action log
            return None

        try:
            actions_list = json.loads(actions_json_str)  # Load the action JSON string into a Python list of dictionaries
        except json.JSONDecodeError as e:
            error_message = f"Warning: Invalid JSON format in LLM response. Error: {e}"
            print(error_message)
            self.agent_action_log.append(self.format_error_message(error_message, response)) # Add the error message to the agent's action log
            return None

        # Iterate through the list of action dictionaries
        for action_dict in actions_list:
            # Extract the action name and parameters from the dictionary
            action_name = action_dict.get("function")
            parameters = action_dict.get("arguments", {})

            # Find the corresponding action object using the ActionInterface instance
            action_obj = self.get_action(action_name)

            # If the action object is not found, print a warning and skip to the next action
            if action_obj is None:
                error_message = f"Warning: Unknown action: {action_name}"
                print(error_message)
                self.agent_action_log.append(self.format_error_message(error_message, response)) # Add the error message to the agent's action log
                continue

            if action_obj.action_set_object is not None:
                parameters["action_set_object"] = action_obj.action_set_object

            # Find the corresponding action object using the ActionInterface instance
            action_obj = self.get_action(action_name)

            # perform the action
            try:
                action_output = action_obj.perform(**parameters)
            except Exception as e:
                error_message = f"Warning: Error performing action {action_name}. Error: {e}"
                print(error_message)
                self.agent_action_log.append(self.format_error_message(error_message, response))
                continue

            # Add the action to the agent's action log
            self.agent_action_log.append(self.format_action(action_obj, parameters, action_output))

    def format_action(self, action_obj, parameters, action_output):
        """
        Formats the action and its output into a string that can be displayed in the LLM prompt's agent action log section.

        # TODO: summarize the action output if it is too long
        """
        # replace the task object in parameters with the task description
        if "task" in parameters:
            parameters["task"] = parameters["task"].description
        
        action_str = f"Action: {action_obj.name}\n"
        action_str += f"Parameters: {parameters}\n"
        action_str += f"Output: {action_output}"
        return action_str
    
    def format_error_message(self, error_message, raw_response):
        """
        Formats the error message into a string that can be displayed in the LLM prompt's agent action log section.
        """
        error_str = f"ERROR performing action\n{error_message}\n"
        error_str += f"Your response that led to this error:\n`{raw_response}`"
        return error_str
    
    def format_agent_action_log(self):
        """
        Formats the agent's action log into a string that can be displayed in the LLM prompt's agent action log section.

        # TODO: add a parameter to specify how many actions to display
        """
        num_actions_to_display = 10
        agent_action_log_str = ""
        for action_str in self.agent_action_log[-num_actions_to_display:]:
            agent_action_log_str += f"{action_str}\n\n"
        return agent_action_log_str.strip()
    
    def format_response(self, response):
        """
        Formats the LLM response into a string that is suitable for displaying to the user.
        """
        # extract the scratchpad from the response (everything between 'Part 1) Temporary scratchpad' and 'Part 2) Action requests')
        scratchpad = response[response.find("Part 1) Temporary scratchpad") + len("Part 1) Temporary scratchpad"):response.find("Part 2) Action requests")].strip()
        return scratchpad

    
# create list of Action objects from a list of ActionSet objects
def get_action_list(action_sets):
    action_list = []
    for action_set in action_sets:
        action_list.extend(action_set.action_list)
    return action_list


RESPONSE_FORMATTING_INSTRUCTIONS = """
Your response MUST follow the following two-part format: 1) scratchpad, 2) action requests list. The program that parses your response is a simple program, not an AI, so if you do not follow the required format exactly it will cause errors.

Part 1) Temporary scratchpad
You have found that writing out your thoughts and reasoning prior to deciding which actions to take helps you make better decisions. This is especially true when you’re trying to solve complex problems that require substantial reasoning. Any text you write in this section of your response will be ignored by the system that parses your action requests, so this is just for your own internal use. Also note that the text in this section will not be saved, which means you won't be able to see it or remember it after this response. 

For any actions you want to take, you MUST specify them in Part 2.

Part 2) Action requests list
This is where you specify the actions you want to take. Use the following list of dictionaries format to specify your actions. Be sure to use valid Python syntax for any parameters and to include all required parameters for each function call. You must request at least one action, and you can request as many as five actions. Do not include any text in this section outside of the list, because it will be ignored. Here is the format to follow:
[
    {{
        "function": "action_name_1",
        "arguments": {{
            "parameter_1": "value_1",
            "parameter_2": "value_2",
            ...
        }}
    }},
    {{
        "function": "action_name_2",
        "arguments": {{
            "parameter_1": "value_1",
            "parameter_2": "value_2",
            ...
        }}
    }},
    ...
]

The actions will be performed in the order that you specify them. Please be sure to use the exact names of the functions and parameters as they appear in the AVAILABLE ACTIONS section above. And be sure to use the list of dictionaries format to specify the functions and parameters. Do not actually try to call the function itself. Do not respond with anything other than your scratchpad and the list of functions you want to call, as adding any additional text to your response will cause an error.

""".strip()


"""
# create action interface
from task_tree_management import task_tree_management_action_set
#action_interface = create_action_interface(action_sets=[task_tree_management_action_set])
action_interface = ActionInterface(action_sets=[task_tree_management_action_set])
available_actions_str = action_interface.get_available_actions_for_prompt()
print(available_actions_str)
"""