from mcp.server.fastmcp import FastMCP
from typing import Optional, List
import requests
from uuid import UUID


AI_BACKEND_URL = "http://localhost:8000"

mcp = FastMCP("hello-server")


FAKE_USERS_DB = [
    {
        "id": "u001",
        "name": "Nguyễn Văn A",
        "email": "a.nguyen@example.com",
        "role": "user",
        "balance": 120000,
        "created_at": "2024-08-01",
    },
    {
        "id": "u002",
        "name": "Trần Thị B",
        "email": "b.tran@example.com",
        "role": "admin",
        "balance": 500000,
        "created_at": "2023-12-15",
    },
]


@mcp.tool(
    description="""
This tool generates a laboratory test CRF form.

STRICT SCHEMA RULES (MUST FOLLOW):
- All fields must strictly follow the provided schema.
- The `type` field of each laboratory test item MUST be one of the following values ONLY:
  - "textarea"
  - "number"
  - "date"
  - "time"
  - "dateTime"
  - "radio"
  - "checkbox"
  - "single-select"
  - "multiple-select"
  - "text"
  - "file"

DO NOT invent new types.
DO NOT use synonyms such as "string", "int", "select", "dropdown", or "boolean".

LABORATORY TEST ITEM RULES:
Each item MUST include:
- label: a human-readable name.
- code: a machine-readable identifier (no spaces).
- type: one of the allowed input types.
- options:
  - REQUIRED and MUST be NON-EMPTY when type is one of:
    "radio", "checkbox", "single-select", "multiple-select".
  - MUST be an empty list [] for all other types.

DO NOT include options for types that do not support options.

ATTACHMENT RULE:
- `attachment_uid` is required and identifies the file or CRF context used to generate the laboratory test form.

If any field violates these rules, DO NOT call the tool.
Revise the output until it fully complies with the schema.

EXAMPLE VALID INPUT:
{
  "items": [
    {
      "label": "Blood Type",
      "code": "BLOOD_TYPE",
      "type": "single-select",
      "unit": null,
      "options": [
        {"label": "A", "value": "A"},
        {"label": "B", "value": "B"},
        {"label": "AB", "value": "AB"},
        {"label": "O", "value": "O"}
      ]
    }
  ],
  "user_prompt": [
    "Generate a laboratory test CRF form based on the provided items."
  ]
}
"""
)
async def laboratory_test(
    attachment_uid: UUID,
    items: Optional[List] = None,
    user_prompt: Optional[List[str]] = None,
) -> dict:
    payload = {
        "items": items or [],
        "user_prompt": user_prompt,
    }

    response = requests.post(
        f"{AI_BACKEND_URL}/api/crfs/laboratory-test/{attachment_uid}",
        json=payload,
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_user_info(
    user_id: Optional[str] = None,
    name: Optional[str] = None,
) -> dict:

    if not user_id and not name:
        return {
            "success": False,
            "error_code": "INVALID_PARAMS",
            "message": "Cần truyền user_id hoặc name",
        }

    if user_id:
        for user in FAKE_USERS_DB:
            if user["id"] == user_id:
                return {"success": True, "data": user}
        return {"success": False, "error": "USER_NOT_FOUND"}

    name_lower = name.lower()
    matched = [
        u for u in FAKE_USERS_DB
        if name_lower in u["name"].lower()
    ]

    if not matched:
        return {"success": False, "error": "USER_NOT_FOUND"}

    return {"success": True, "data": matched}

if __name__ == "__main__":
    mcp.run()
