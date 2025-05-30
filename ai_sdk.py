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

def extract_table_from_image(
    images_base64: List[str],
    additional_prompt: str = "",
    model: str = "claude-3-5-sonnet-20241022",
):
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

