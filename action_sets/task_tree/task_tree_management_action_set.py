from task_class import Task

# action functions for editing the task tree
def break_into_subtasks(task: Task, subtask_descriptions: list[str]):
    for description in subtask_descriptions:
        subtask = Task(description=description, parent=task)
        task.add_subtask(subtask)

def mark_current_task_as_complete(task):
    task.complete = True

def edit_task_description(task: Task, task_index: int, new_description: str):
    # TODO: add error handling for invalid task_index or task_index below the current task
    if task.parent:
        if task_index == 0:
            task.parent.description = new_description
        elif task_index > 0:
            task.parent.subtasks[task_index-1].description = new_description


# available actions for editing the task tree, with descriptions and formatting instructions; this goes in the prompt
task_tree_management_actions_list = [
    {
        "name": "break_into_subtasks(subtask_descriptions: list[str])",
        "function": break_into_subtasks,
        "when_to_use": "Use this function to break the current task into a list of subtasks.",
        "arguments": "Arguments:\n  - subtask_descriptions (list): This should be a list of strings, with each string specifying a subtask. The subtask strings should be provided in the order you would like to perform the tasks in."
    },
    {
        "name": "mark_current_task_as_complete()",
        "function": mark_current_task_as_complete,
        "when_to_use": "Use this function to mark the current task as complete, so you can move on to the next task.",
        "arguments": "Arguments: None. This function takes no arguments, so you must use an empty set of Arguments when calling this function."
    },
    {
        "name": "edit_task_description(task_index: int, new_description: str)",
        "function": edit_task_description,
        "when_to_use": "Use this function to edit the current task, one of the sibling tasks, or the parent task.",
        "arguments": "Arguments:\n  - task_index (int): This is the index of the task that you would like to edit. This uses 1-indexing, so the first sibling task will have index 1, the second task will have index 2, etc. If you want to edit the parent task, use task_index=0. Note that you can only edit sibling tasks that have not yet been completed (i.e. the task index must either be zero, or it must be greater than or equal to the index of the current task).\n  - new_description (str): This is the new task description you would like to use for the task you’re editing. Be sure to provide sufficient detail for the task."
    },
]

task_tree_management_action_set = {"name": "task_tree_management_actions", "actions": task_tree_management_actions_list}