"""
This module defines the interface between the task tree and the SDF

The action_set_object is the SDF Document.
"""

from agent.action_interface import Action, ActionSet

def edit_title(action_set_object, title):
    action_set_object.edit_title(title)

def update_outline(action_set_object, outline):
    action_set_object.update_outline(outline)

def add_character_description(action_set_object, name, description):
    action_set_object.add_character_description(name, description)

def update_character_description(action_set_object, name, description):
    action_set_object.update_character_description(name, description)

def remove_character_description(action_set_object, name):
    action_set_object.remove_character_description(name)

def add_location(action_set_object, name, description):
    action_set_object.add_location(name, description)

def update_location(action_set_object, name, description):
    action_set_object.update_location(name, description)

def remove_location(action_set_object, name):
    action_set_object.remove_location(name)

def add_theme(action_set_object, name, description):
    action_set_object.add_theme(name, description)

def update_theme(action_set_object, name, description):
    action_set_object.update_theme(name, description)

def remove_theme(action_set_object, name):
    action_set_object.remove_theme(name)

def add_section(action_set_object, index, title='', summary=''):
    action_set_object.add_section(index, title, summary)

def move_section(action_set_object, index, direction):
    action_set_object.move_section(index, direction)

def merge_sections(action_set_object, index):
    action_set_object.merge_sections(index)

def split_section(action_set_object, index, split_index, new_title):
    action_set_object.split_section(index, split_index, new_title)

def edit_section(action_set_object, section_index, editing_instructions):
    action_set_object.edit_section(section_index, editing_instructions)

def read_and_analyze_section(action_set_object, section_index, analysis_instructions):
    return action_set_object.read_and_analyze_section(section_index, analysis_instructions)


writing_actions_list = [
    Action(
        name="edit_title(title)",
        when_to_use="Use this function to edit the title of the document.",
        arguments="Arguments:\n  - title: The new title of the document.",
        action_function=edit_title
    ),
    Action(
        name="update_outline(outline)",
        when_to_use="Use this function to update the outline of the document.",
        arguments="Arguments:\n  - outline: The updated outline text.",
        action_function=update_outline
    ),
    Action(
        name="add_character_description(name, description)",
        when_to_use="Use this function to add a character description to the document.",
        arguments="Arguments:\n  - name: The name of the character.\n  - description: The character description.",
        action_function=add_character_description
    ),
    Action(
        name="update_character_description(name, description)",
        when_to_use="Use this function to update a character description in the document.",
        arguments="Arguments:\n  - name: The name of the character.\n  - description: The updated character description.",
        action_function=update_character_description
    ),
    Action(
        name="remove_character_description(name)",
        when_to_use="Use this function to remove a character description from the document.",
        arguments="Arguments:\n  - name: The name of the character to remove.",
        action_function=remove_character_description
    ),
    Action(
        name="add_location(name, description)",
        when_to_use="Use this function to add a location description to the document.",
        arguments="Arguments:\n  - name: The name of the location.\n  - description: The location description.",
        action_function=add_location
    ),
    Action(
        name="update_location(name, description)",
        when_to_use="Use this function to update a location description in the document.",
        arguments="Arguments:\n  - name: The name of the location.\n  - description: The updated location description.",
        action_function=update_location
    ),
    Action(
        name="remove_location(name)",
        when_to_use="Use this function to remove a location description from the document.",
        arguments="Arguments:\n  - name: The name of the location to remove.",
        action_function=remove_location
    ),
    Action(
        name="add_theme(name, description)",
        when_to_use="Use this function to add a theme description to the document.",
        arguments="Arguments:\n  - name: The name of the theme.\n  - description: The theme description.",
        action_function=add_theme
    ),
    Action(
        name="update_theme(name, description)",
        when_to_use="Use this function to update a theme description in the document.",
        arguments="Arguments:\n  - name: The name of the theme.\n  - description: The updated theme description.",
        action_function=update_theme
    ),
    Action(
        name="remove_theme(name)",
        when_to_use="Use this function to remove a theme description from the document.",
        arguments="Arguments:\n  - name: The name of the theme to remove.",
        action_function=remove_theme
    ),
    Action(
        name="add_section(index, title='', summary='')",
        when_to_use="Use this function to add a new section to the document.",
        arguments="Arguments:\n  - index: The index at which to insert the new section. Note: sections are zero-indexed, so the first section will be index 0, etc.\n  - title: The title of the new section (optional).\n  - summary: The summary of the new section (optional).",
        action_function=add_section
    ),
    Action(
        name="move_section(index, direction)",
        when_to_use="Use this function to move a section in the document.",
        arguments="Arguments:\n  - index: The index of the section to move.\n  - direction: The direction to move the section (1 for down, -1 for up).",
        action_function=move_section
    ),
    Action(
        name="merge_sections(index)",
        when_to_use="Use this function to merge two sections in the document.",
        arguments="Arguments:\n  - index: The index of the first section to merge.",
        action_function=merge_sections
    ),
    Action(
        name="split_section(index, split_index, new_title)",
        when_to_use="Use this function to split a section in the document.",
        arguments="Arguments:\n  - index: The index of the section to split.\n  - split_index: The index of the element to split on.\n  - new_title: The title of the new section, which will be inserted after the current section.",
        action_function=split_section
    ),
    Action(
        name="edit_section(section_index, editing_instructions)",
        when_to_use="Use this function to add to or edit the text for a specific section of the document. This function calls another LLM that's been fine-tuned for writing, and that has access to the full text of the section. When you call edit_section, you just need to provide editing instructions, so that this special-purpose LLM knows what to do. Note: you must create a section (by using the add_section function) before you can edit it.",
        arguments="Arguments:\n  - section_index: The index of the section to edit. Note: sections are zero-indexed, so the first section will be index 0, etc.\n  - editing_instructions: Natural language instructions describing the additions or edits to be made.",
        action_function=edit_section
    ),
    Action(
        name="read_and_analyze_section(section_index, analysis_instructions)",
        when_to_use="Use this function to read and analyze a specific section of the document. This function calls another LLM that's been fine-tuned for reading, and that has access to the full text of the section. When you call read_and_analyze_section, you just need to provide analysis instructions, so that this special-purpose LLM knows what to do. Keep in mind that this function can only analyze one section at a time. If you want to analyze multiple sections, you'll need to call this function multiple times. This is the only method you have to read what you write, so be sure to use it frequently!",
        arguments="Arguments:\n  - section_index: The index of the section to read and analyze. Note: sections are zero-indexed, so the first section will be index 0, etc.\n  - analysis_instructions: Natural language instructions describing the analysis to be performed. Be clear about what exactly you want to analyze.",
        action_function=read_and_analyze_section
    ),
]

writing_action_set = ActionSet(action_list=writing_actions_list, action_set_name="writing_action_set", action_set_object=None)