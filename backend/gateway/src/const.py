from typing import Literal


LIST_MODE = Literal["paginated", "all"]
TAGS_METADATA = [
    {
        "name": "Authorization",
        "description": "Grant Access.",
    },
    {
        "name": "User Management",
        "description": "Verify Identity & Grant Access",
    },
    {
        "name": "Health Checker",
        "description": "Verify Availability",
    },
]
