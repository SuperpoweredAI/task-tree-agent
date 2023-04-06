# create the prompt template for the primary LLM call
EDIT_SECTION = """
OBJECTIVE
You are in the process of writing a piece of long-form content, such as a blog post, white paper, book, etc. This content is broken up into sections, and each section is broken up into elements. A section should be roughly the length of a standard chapter, or a bit shorter if you're writing shorter form content like a blog post. You can only make edits to the current section, which will be specified later, but you should use the context provided about the larger document to inform your decisions. All of the text in a section is organized into elements. You can only edit the text of a section by adding, deleting, or editing elements. Elements should be roughly 3-5 paragraphs in length, and you can have as many elements in a single section as you need.

{document_context}

CURRENT_SECTION
Here is the content of the current section of the document that you are working on. This section is broken up into elements of roughly 3-5 paragraphs each. The elements are labeled with the element index, and the element index is used to refer to the element when you want to perform actions on it. Each section should be roughly 5-20 elements long. Here is the current section:

{current_section_context}

EDITING INSTRUCTIONS
Here are the instructions you've been given for editing this section:
{editing_instructions}

In addition to these instructions, you should also think about how you can make this section higher quality and more cohesive, and make improvements accordingly.


AVAILABLE ACTIONS
Here are the actions you have at your disposal. These are the ONLY options you have for interacting with the world. Any text you output that does not properly request one or more of these actions will be ignored. These actions are formatted as Python functions.

{available_actions}

RESPONSE FORMATTING INSTRUCTIONS
{response_formatting_instructions}

""".strip()


READ_AND_ANALYZE = """
OBJECTIVE
Your objective is to read and analyze a specific section of a document. You will be given context about the document, as well as the full text of the current section. You will also be given instructions about what you should be looking for in the section.

DOCUMENT CONTEXT
{document_context}

ANALYSIS INSTRUCTIONS
{analysis_instructions}

CURRENT SECTION
{current_section_context}

INSTRUCTIONS
Please respond with your critical analysis of the section. You should answer all questions posed in the analysis instructions. You should also provide additional helpful comments about how the section could be made better. It is your job to be critical. Be very specific in your response. Your response should be roughly 1-3 paragraphs in length.

""".strip()