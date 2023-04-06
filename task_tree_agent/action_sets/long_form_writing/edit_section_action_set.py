"""
action_set_object is the Section object this is being edited.
"""
import os
import sys

# add task_tree_agent to the path. It's not installed as a package, so we need to add it to the path manually.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "task_tree_agent"))

from agent.action_interface import Action, ActionSet

# Action functions for the edit_section function
def add_element(action_set_object, element_index: int, content: str):
    # validate arguments
    if element_index < 0 or element_index > len(action_set_object.elements):
        raise ValueError("The element index is invalid.")
    if not isinstance(content, str):
        raise TypeError("The content must be a string.")
    if not content:
        raise ValueError("The content cannot be empty.")
    if not isinstance(element_index, int):
        raise TypeError("The element index must be an integer.")
    action_set_object.add_element(element_index, content)

def edit_element(action_set_object, element_index: int, content: str):
    action_set_object.edit_element(element_index, content)

def delete_element(action_set_object, element_index: int):
    action_set_object.delete_element(element_index)

def update_section_title(action_set_object, new_title: str):
    action_set_object.title = new_title

def update_section_summary(action_set_object, new_section_summary: str):
    action_set_object.section_summary = new_section_summary

def update_section_outline(action_set_object, new_section_outline: str):
    action_set_object.section_outline = new_section_outline


sdf_action_list = [
    Action(
        name="add_element(element_index, content)",
        when_to_use="Use this when you want to add an element to a action_set_object",
        arguments="Arguments:\n  - element_index (int): This is the index to specify the location in the action_set_object that you would like this element to be placed in. For example, to add an element to the beginning of the action_set_object, use 0 for the element_index.\n  - content (str): This is the content of the element you would like to add. Elements should generally be 3-5 paragraphs long. You can use double new line characters to separate paragraphs within an element.",
        action_function=add_element,
    ),
    Action(
        name="edit_element(element_index, content)",
        when_to_use="Use this when you would like to edit an element in a action_set_object.",
        arguments="Arguments:\n - element_index (int): This is the index of the element that you would like to edit.\n - content (str): This is the content that you would like to use for the element. This will replace the existing content.",
        action_function=edit_element,
    ),
    Action(
        name="delete_element(element_index)",
        when_to_use="Use this function to delete an element from the action_set_object.",
        arguments="Arguments:\n  - element_index (int): This is the index of the element that you would like to delete.",
        action_function=delete_element,
    ),
    Action(
        name="update_section_title(new_title)",
        when_to_use="Use this when you would like to update the title of the action_set_object.",
        arguments="Arguments:\n - new_title (str): This is the new title you would like to use for the action_set_object.",
        action_function=update_section_title,
    ),
    Action(
        name="update_section_summary(new_section_summary)",
        when_to_use="Use this when you would like to update the summary of the action_set_object. Whenever the action_set_object content has been substantially changed, you should update the summary to reflect the new content.",
        arguments="Arguments:\n - new_section_summary (str): This is the new summary you would like to use for the action_set_object. The summary should be pretty short.",
        action_function=update_section_summary,
    ),
    Action(
        name="update_section_outline(new_section_outline)",
        when_to_use="Use this when you would like to update the outline of the action_set_object. You should ALWAYS create a detailed action_set_object outline before starting to write a action_set_object. Whenever the action_set_object content has been substantially changed, you should update the outline to reflect the new content.",
        arguments="Arguments:\n - new_section_outline (str): This is the new outline you would like to use for the action_set_object. A good outline is very detailed and includes information about all the major things that are going to happen in the action_set_object, as well as additional information like character development, plot points, themes, etc.",
        action_function=update_section_outline,
    )
]

edit_section_action_set = ActionSet(action_list=sdf_action_list, action_set_name="edit_section_action_set", action_set_object=None)