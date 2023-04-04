# Action functions for the edit_section function
def add_element(section, element_index: int, content: str):
    # validate arguments
    if element_index < 0 or element_index > len(section.elements):
        raise ValueError("The element index is invalid.")
    if not isinstance(content, str):
        raise TypeError("The content must be a string.")
    if not content:
        raise ValueError("The content cannot be empty.")
    if not isinstance(element_index, int):
        raise TypeError("The element index must be an integer.")
    section.add_element(element_index, content)

def edit_element(section, element_index: int, content: str):
    section.edit_element(element_index, content)

def delete_element(section, element_index: int):
    section.delete_element(element_index)

def update_section_title(section, new_title: str):
    section.title = new_title

def update_section_summary(section, new_section_summary: str):
    section.section_summary = new_section_summary

def update_section_outline(section, new_section_outline: str):
    section.section_outline = new_section_outline


# available actions for editing a section, with descriptions and formatting instructions; this goes in the prompt
sdf_action_list = [
    {
        "name": "add_element(element_index, content)",
        "function": add_element,
        "when_to_use": "Use this when you want to add an element to a section",
        "arguments": "Arguments:\n  - element_index (int): This is the index to specify the location in the section that you would like this element to be placed in. For example, to add an element to the beginning of the section, use 0 for the element_index.\n  - content (str): This is the content of the element you would like to add. Elements should generally be 3-5 paragraphs long. You can use double new line characters to separate paragraphs within an element."
    },
    {
        "name": "edit_element(element_index, content)",
        "function": edit_element,
        "when_to_use": "Use this when you would like to edit an element in a section.",
        "arguments": "Arguments:\n - element_index (int): This is the index of the element that you would like to edit.\n - content (str): This is the content that you would like to use for the element. This will replace the existing content."
    },
    {
        "name": "delete_element(element_index)",
        "function": delete_element,
        "when_to_use": "Use this function to delete an element from the section.",
        "arguments": "Arguments:\n  - element_index (int): This is the index of the element that you would like to delete."
    },
    {
        "name": "update_section_title(new_title)",
        "function": update_section_title,
        "when_to_use": "Use this when you would like to update the title of the section.",
        "arguments": "Arguments:\n - new_title (str): This is the new title you would like to use for the section."
    },
    {
        "name": "update_section_summary(new_section_summary)",
        "function": update_section_summary,
        "when_to_use": "Use this when you would like to update the summary of the section. Whenever the section content has been substantially changed, you should update the summary to reflect the new content.",
        "arguments": "Arguments:\n - new_section_summary (str): This is the new summary you would like to use for the section. The summary should be pretty short."
    },
    {
        "name": "update_section_outline(new_section_outline)",
        "function": update_section_outline,
        "when_to_use": "Use this when you would like to update the outline of the section. You should ALWAYS create a detailed section outline before starting to write a section. Whenever the section content has been substantially changed, you should update the outline to reflect the new content.",
        "arguments": "Arguments:\n - new_section_outline (str): This is the new outline you would like to use for the section. A good outline is very detailed and includes information about all the major things that are going to happen in the section, as well as additional information like character development, plot points, themes, etc."
    }
]

edit_section_action_set = {"name": "sdf_action_set", "actions": sdf_action_list}