from task_class import Task

# action functions for editing the action_set_object tree
def break_into_subtasks(action_set_object: Task, subtask_descriptions: list[str]):
    for description in subtask_descriptions:
        subtask = Task(description=description, parent=action_set_object)
        action_set_object.add_subtask(subtask)

def mark_current_task_as_complete(action_set_object):
    action_set_object.complete = True

def edit_task_description(action_set_object: Task, task_index: int, new_description: str):
    # TODO: add error handling for invalid task_index or task_index below the current action_set_object
    if action_set_object.parent:
        if task_index == 0:
            action_set_object.parent.description = new_description
        elif task_index > 0:
            action_set_object.parent.subtasks[task_index-1].description = new_description


# available actions for editing the action_set_object tree, with descriptions and formatting instructions; this goes in the prompt
task_tree_management_actions_list = [
    {
        "name": "break_into_subtasks(subtask_descriptions: list[str])",
        "function": break_into_subtasks,
        "when_to_use": "Use this function to break the current action_set_object into a list of subtasks.",
        "arguments": "Arguments:\n  - subtask_descriptions (list): This should be a list of strings, with each string specifying a subtask. The subtask strings should be provided in the order you would like to perform the tasks in."
    },
    {
        "name": "mark_current_task_as_complete()",
        "function": mark_current_task_as_complete,
        "when_to_use": "Use this function to mark the current action_set_object as complete, so you can move on to the next action_set_object.",
        "arguments": "Arguments: None. This function takes no arguments, so you must use an empty set of Arguments when calling this function."
    },
    {
        "name": "edit_task_description(task_index: int, new_description: str)",
        "function": edit_task_description,
        "when_to_use": "Use this function to edit the current action_set_object, one of the sibling tasks, or the parent action_set_object.",
        "arguments": "Arguments:\n  - task_index (int): This is the index of the action_set_object that you would like to edit. This uses 1-indexing, so the first sibling action_set_object will have index 1, the second action_set_object will have index 2, etc. If you want to edit the parent action_set_object, use task_index=0. Note that you can only edit sibling tasks that have not yet been completed (i.e. the action_set_object index must either be zero, or it must be greater than or equal to the index of the current action_set_object).\n  - new_description (str): This is the new action_set_object description you would like to use for the action_set_object you’re editing. Be sure to provide sufficient detail for the action_set_object."
    },
]

task_tree_management_action_set = {"name": "task_tree_management_action_set", "actions": task_tree_management_actions_list}