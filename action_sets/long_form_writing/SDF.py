"""
The following module contains the classes for the SDF document format, which is used to represent a long-form document in a way that is easy for LLMs to understand and manipulate.

This is an example of creating an action set that itself uses an agent w/ tools framework, which is why we import the ActionInterface class.
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir+'/../../agent')

from utils import openai_api_call
from action_interface import ActionInterface, RESPONSE_FORMATTING_INSTRUCTIONS
from edit_section_action_set import edit_section_action_set
from SDF_prompt_template import EDIT_SECTION, READ_AND_ANALYZE

class Element:
    def __init__(self, content):
        self.content = content


class Section:
    def __init__(self, section_identifier='', title='', summary=''):
        self.section_identifier = section_identifier # e.g., "Chapter 1"
        self.title = title
        self.summary = summary
        self.outline = ""
        self.elements = []

    # add new element to the section
    def add_element(self, index, content):
        element = Element(content)
        self.elements.insert(index, element)

    # edit an existing element
    def edit_element(self, index, content):
        self.elements[index].content = content

    # delete an element
    def delete_element(self, index):
        del self.elements[index]

    # re-order elements, given a list of indices
    def reorder_elements(self, indices):
        self.elements = [self.elements[i] for i in indices]

    # get the word count of the section
    def get_word_count(self):
        count = 0
        for element in self.elements:
            count += len(element.content.split())
        return count

    # display the section
    def display(self):
        print(f"\n# {self.title}")
        for i,element in enumerate(self.elements):
            print(f"\nElement {i}\n{element.content}")


class Document:
    def __init__(self, title, human_notes="", section_type='Section', model_name="gpt-4"):
        self.title = title
        self.human_notes = human_notes
        self.section_type = section_type
        self.sections = []
        self.table_of_contents = []
        self.outline = ""
        self.character_descriptions = {}
        self.locations = {}
        self.themes = {}
        self.action_interface = ActionInterface([edit_section_action_set])
        self.model_name = model_name # e.g., "gpt-4", the model used to generate text in edit_section()

    def edit_title(self, title):
        self.title = title

    def update_outline(self, outline):
        self.outline = outline

    # Character descriptions methods
    def add_character_description(self, name, description):
        self.character_descriptions[name] = description

    def update_character_description(self, name, description):
        if name in self.character_descriptions:
            self.character_descriptions[name] = description

    def remove_character_description(self, name):
        if name in self.character_descriptions:
            del self.character_descriptions[name]

    # Locations methods
    def add_location(self, name, description):
        self.locations[name] = description

    def update_location(self, name, description):
        if name in self.locations:
            self.locations[name] = description

    def remove_location(self, name):
        if name in self.locations:
            del self.locations[name]

    # Themes methods
    def add_theme(self, name, description):
        self.themes[name] = description

    def update_theme(self, name, description):
        if name in self.themes:
            self.themes[name] = description

    def remove_theme(self, name):
        if name in self.themes:
            del self.themes[name]

    # Sections methods
    def add_section(self, index, title='', summary=''):
        # validate index
        if index < 0 or index > len(self.sections):
            return None
        
        # create new section
        section_identifier = f"{self.section_type} {index + 1}"
        section = Section(section_identifier, title, summary)
        self.sections.insert(index, section)
        
        # update section identifiers
        for i in range(len(self.sections)):
            self.sections[i].section_identifier = f"{self.section_type} {i + 1}"

        self.update_toc() # update table of contents

    # find the index of a section by section identifier
    def find_section_index(self, section_identifier):
        section_identifier = section_identifier.strip()
        for i in range(len(self.sections)):
            if self.sections[i].section_identifier == section_identifier:
                return i
        return None

    def move_section(self, index, direction):
        if 0 <= index < len(self.sections) and 0 <= index + direction < len(self.sections):
            self.sections[index], self.sections[index + direction] = self.sections[index + direction], self.sections[index]
            
            # update section identifiers
            for i in range(len(self.sections)):
                self.sections[i].section_identifier = f"{self.section_type} {i + 1}"

            self.update_toc() # update table of contents

    def merge_sections(self, index):
        if 0 <= index < len(self.sections) - 1:
            self.sections[index].title += f" - {self.sections[index + 1].title}"
            self.sections[index].elements += self.sections[index + 1].elements
            self.sections[index].subsections += self.sections[index + 1].subsections
            del self.sections[index + 1]
            
            # update section identifiers
            for i in range(len(self.sections)):
                self.sections[i].section_identifier = f"{self.section_type} {i + 1}"
            
            self.update_toc() # update table of contents

    def split_section(self, index, split_index, new_title):
        """
        - split_index is the index of the element to split on
        - new_title is the title of the new section, which will be inserted after the current section
        """
        if 0 <= index < len(self.sections):
            new_section = Section(new_title)
            new_section.elements = self.sections[index].elements[split_index:]
            self.sections[index].elements = self.sections[index].elements[:split_index]
            self.sections.insert(index + 1, new_section)

            # update section identifiers
            for i in range(len(self.sections)):
                self.sections[i].section_identifier = f"{self.section_type} {i + 1}"
            
            self.update_toc() # update table of contents

    def get_word_count(self):
        count = 0
        for section in self.sections:
            count += section.get_word_count()
        return count

    def update_toc(self):
        self.table_of_contents = [section.title for section in self.sections]

    # create a context string to be used in the prompt
    def format_prompt_context(self):

        # Generate the prompt, starting with the human notes
        context_str = f"The following are some human-written notes about the document you're writing. You should pay careful attention to these notes and stick closely to any ideas conveyed in them.\n\nHuman Notes:\n{self.human_notes}\n\n"

        context_str += "Document Overview:\n"

        # add title
        context_str += f"Title: {self.title}\n\n"

        # add outline
        context_str += "Outline:\n"
        context_str += self.outline + "\n"

        # add word count
        context_str += f"\nWord Count: {self.get_word_count()}\n"

        context_str += "\nSection Summaries:\n"
        for section in self.sections:
            context_str += f"{section.section_identifier} - {section.title}:\n{section.summary}\n\n"

        context_str += "\nCharacter Descriptions:\n"
        for name, description in self.character_descriptions.items():
            context_str += f"{name}: {description}\n"

        context_str += "\nLocations:\n"
        for name, description in self.locations.items():
            context_str += f"{name}: {description}\n"

        context_str += "\nThemes:\n"
        for name, description in self.themes.items():
            context_str += f"{name}: {description}\n"

        return context_str

    def format_section_for_prompt(self, section_index):
        if section_index != None:
            current_section = self.sections[section_index]
        else:
            current_section = None

        if current_section is None:
            return None

        # put all the information needed about the current section into a string
        context_str = f"\nCurrent Section: {current_section.section_identifier} - {current_section.title}\n\n"
        context_str += f"Section Summary:\n{current_section.summary}\n\n"
        context_str += f"Section Outline:\n{current_section.outline}\n\n"
        context_str += f"Section Word Count: {current_section.get_word_count()}\n\n"
        context_str += "Section Full Text:\n"
        for i,element in enumerate(current_section.elements):
            context_str += f"Element: {i}\n{element.content}\n\n"
        
        return context_str

    def create_edit_section_prompt(self, section_index, editing_instructions):
        document_context = self.format_prompt_context() # Create the document context string
        if document_context is None:
            return None
        current_section_context = self.format_section_for_prompt(section_index) # Create the current section context string

        available_actions = self.action_interface.get_available_actions_for_prompt()

        return EDIT_SECTION.format(
            document_context=document_context,
            editing_instructions=editing_instructions,
            current_section_context=current_section_context,
            available_actions=available_actions,
            response_formatting_instructions=RESPONSE_FORMATTING_INSTRUCTIONS,
        )
    
    def edit_section(self, section_index: str, editing_instructions: str, verbose: bool = False):
        """
        This is the main function we will use to edit the document.

        The editing instructions is a natural language string that describes the edit we want the LLM to make.
        """
        prompt = self.create_edit_section_prompt(section_index, editing_instructions)
        self.action_interface.update_action_set_object("edit_section_action_set", self.sections[section_index])
        response = openai_api_call(prompt, model_name=self.model_name, max_tokens=2000)

        if verbose:
            print(f"Full prompt:\n{prompt}")
            print(f"Raw LLM response:\n{response}")

        self.action_interface.parse_response_and_perform_actions(response)

    def create_read_and_analyze_prompt(self, section_index, analysis_instructions):
        document_context = self.format_prompt_context()
        if document_context is None:
            return None
        current_section_context = self.format_section_for_prompt(section_index)
        
        return READ_AND_ANALYZE.format(
            document_context=document_context,
            analysis_instructions=analysis_instructions,
            current_section_context=current_section_context,
        )

    def read_and_analyze_section(self, section_index: str, analysis_instructions: str, verbose: bool = False):
        prompt = self.create_read_and_analyze_prompt(section_index, analysis_instructions)
        analysis = openai_api_call(prompt, model_name=self.model_name, max_tokens=500)

        if verbose:
            print(f"Full prompt:\n{prompt}")
            print(f"Raw LLM response:\n{analysis}")
        
        return analysis.strip()

    def display(self):
        print(f"Title: {self.title}")
        print("\nTable of Contents:")
        for section in self.sections:
            print(f"{section.section_identifier} - {section.title}") 

        print("\nSections:")
        for section in self.sections:
            section.display()