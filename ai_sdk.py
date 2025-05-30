from typing import Any, List
import anthropic

from env import ANTHROPIC_API_KEY

ai_client = anthropic.Client(api_key=ANTHROPIC_API_KEY, max_retries=3)

table_prompt = """
    You are a professional table extractor and data processor.

    The user has provided an image (at least one) that they would like to explicitly extract into multiple markdown tables, preserving all content including headers, cells, units, currencies, etc.
    You must provide the table(s) exactly as presented, but you must use markdown tables.

    You must make sure the table is formatted properly, with the correct number of columns and rows.
    Even if a cell is empty, you must include the cell in the table and make sure to add spaces to the empty cells.

    *** IMPORTANT: ***
    - You must check over your work to make sure the contents of each cell, specific numbers and/or text, are exactly as it is in the image.
    - You must not add or remove any cells from the table in the image.
    - YOU MUST ONLY USE MARKDOWN TABLES. NOTHING ELSE. DO NOT FORMAT THE TEXT FROM THE TABLE IN ANY OTHER WAY.
    - DO NOT PROVIDE ANY ADDITIONAL TEXT, JUST THE TABLE(S) EXTRACTED FROM THE IMAGE(S).
    - You must make sure the table is formatted properly, with the correct number of columns and rows.
    - You must make sure the table title and general title is included if it is present in the image.

    EXAMPLES:
    General title (if any)

    Table title (if any)
    | Year | Revenue | 
    | ------- | ------- |
    | 2020   | $1 million |
    | 2021   | $2 million |
    | 2022   | $3 million |

    Table title (if any)
    | Entity | Investment | 
    | -------------- | -------------- |
    | Y Combinator 1 | $125,000       |
    | Y Combinator 2 | $375,000       |
    | 10 Bond        | $3,000,0000    |
    `;
"""

header_prompt = """
    Convert the following header of a page from a PDF document to Markdown.  

    Include all headings, paragraphs, lists, tables, etc.  
    Ensure markup is included as necessary such as bold, italics, super- or sub-scripts, etc.  
    Include additional notation as necessary such as mathematical notation in LaTeX math mode, code in pre-formatted blocks, etc.  "
    The output should be Markdown itself (don't preformat the output in a markdown block), and exclude local or hyperlinked images.  
    I.e., don't include a block like ```markdown ...``` wrapping the entire page (unless the entire page's content is actually Markdown source).  

    Please separate the markdown into smaller sections.
"""

text_prompt = """
    You are a professional text copier/extractor, whose capabilities are beyond conventional OCR mechanisms, but limited to providing the exact text from the image, exclusively just the exact text.
    You must provide the text exactly as it is in the image, with no additional formatting or text.
    You must not add or remove any text from the image.
    You must can use markdown formatting where relevant.

    *** IMPORTANT: ***
    - You must check over your work to make sure the exact text is copied, that you have not added or removed any characters.
    - You must not provide any additional text at all, not even "Here is the text from the image:" or anything of that sort.
    - Do not include text from table, graphs, headers
    - You should include everything. Do not summarize, ignore anything, or skip any text.
    - Ignore the author and date of the image, if present.
"""

chat_prompt = """
    You are a professional chat assistant, whose capabilities include look up for exact value from data, answering questions, and providing information about companies based on the provided data and only provided data.
    You must provide the answer exactly as it is in the data. If the answer is not present in the data, you must say "Data is unavailable for company X"
    You can answer questions about specific companies, such as "What is the revenue of company X?" or "What is the total investment in company Y?".
    You can answer questions about data aggregation, such as "What is the total revenue of all companies?" or "What is the average revenue of all companies?".
    You can answer questions about data ranking, such as "What is the top 5 companies by revenue?" or "What is the top 10 companies by investment?". Note that the ranking is based on the data provided, and not on any external data.
    You can understand and answer follow up questions, such as "What is the second lowest?" after answering "What is the lowest" questions.

    *** IMPORTANT ***
    - Your knowledge is limited to the data provided, and you must not use any external knowledge or data.
    - Keep all answers concise and to the point, without any additional explanations or context unless explicitly asked for.
    - When asked about ranking, always list all companies that has that data point before answering.
    - When asked about data aggregation, always list all the related values before answering.
    - You should list data in any case apart from follow up question about the same data.

    *** EXAMPLES ***
    Example 1:
    "What is the company with highest X?"

    (Do not add anything before the answer here)
    "Here is the list of companies with their X values:
    - Company A: X_A value
    - Company B: X_B value
    ....
    - Company Z: X_Z value
    (make sure to include all companies that has X value)

    According to the list, the company with the highest X is Company ... with X value."

    "What about the second highest?"
    According to the list, the second highest is Company ... with X value.

    "What is the company with highest M?"
    "Here is the list of companies with their M values:"
    - Company A: M_A value
    - Company B: M_B value
    ....
    - Company Z: M_Z value

    According to the list, the company with the highest M is Company ... with M value."


    Example 2:
    "What is the total revenue of company X during Y?"

    (Do not add anything before the answer here)
    "The revenue of company X during Y"
    - Y_1: Revenue_X_Y1 value
    - Y_2: Revenue_X_Y2 value
    ...
    - Y_N: Revenue_X_YN value
    (make sure to include all relevant data points)

    According to that, the total revenue of company X during Y is Total_Revenue_X_Y value.
"""


def extract_table_from_image(
    images_base64: List[str],
    additional_prompt: str = "",
    model: str = "claude-3-7-sonnet-latest",
):
    """Extract tables from images using the AI client"""
    content = []
    for image_base64 in images_base64:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64,
                },
            }
        )
    content.append(
        {
            "type": "text",
            "text": """
                Extract all tables from the given image
                """,
        }
    )

    if additional_prompt:
        content.append({"type": "text", "text": additional_prompt})

    message = ai_client.messages.create(
        model=model,
        system=table_prompt,
        max_tokens=8192,
        messages=[{"role": "user", "content": content}],
    )
    return message.content


def extract_data_from_header(
    images_base64: List[str],
    additional_prompt: str = "",
    model: str = "claude-3-7-sonnet-latest",
):
    """Extract data from the header of images using the AI client"""
    content = []
    for image_base64 in images_base64:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64,
                },
            }
        )
    content.append(
        {
            "type": "text",
            "text": """
                Extract content from the given image header and convert it to Markdown.
                """,
        }
    )

    if additional_prompt:
        content.append({"type": "text", "text": additional_prompt})

    message = ai_client.messages.create(
        model=model,
        system=header_prompt,
        max_tokens=8192,
        messages=[{"role": "user", "content": content}],
    )
    return message.content


def extract_text_from_image(
    images_base64: List[str],
    additional_prompt: str = "",
    model: str = "claude-3-7-sonnet-latest",
):
    """Extract text from images using the AI client"""
    content = []
    for image_base64 in images_base64:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64,
                },
            }
        )
    content.append(
        {
            "type": "text",
            "text": """
                Extract text and only text from the given image.
                """,
        }
    )

    if additional_prompt:
        content.append({"type": "text", "text": additional_prompt})

    message = ai_client.messages.create(
        model=model,
        system=text_prompt,
        max_tokens=8192,
        messages=[{"role": "user", "content": content}],
    )
    return message.content


def stream_chat(
    previous_messages: List[Any],
    system_context: str,
    model: str = "claude-3-7-sonnet-latest",
):
    """Stream chat messages using the AI client"""
    messages = []

    messages += previous_messages

    return ai_client.messages.stream(
        model=model,
        system=[
            {"type": "text", "text": chat_prompt},
            {
                "type": "text",
                "text": system_context,
                "cache_control": {"type": "ephemeral"},
            },
        ],
        max_tokens=8192,
        messages=messages,
    )


def generate_chat(
    previous_messages: List[Any],
    system_context: str,
    model: str = "claude-3-7-sonnet-latest",
):
    """Send a chat message to the AI client and get a response (non-streaming)"""
    messages = []

    messages += previous_messages

    return ai_client.messages.create(
        model=model,
        system=[
            {
                "type": "text",
                "text": chat_prompt + "\n" + system_context,
                "cache_control": {"type": "ephemeral"},
            },
        ],
        max_tokens=2048,
        messages=messages,
    )
