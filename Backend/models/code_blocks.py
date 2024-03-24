from pydantic import BaseModel


class CodeBlock(BaseModel):
    # id: str
    user_id: str | None
    code_block_name: str
    parent_folder_id: str
    problem_statement: str
    approaches: list
    similar_questions: list


# approachs
# approach
# code
# TC
# SC
