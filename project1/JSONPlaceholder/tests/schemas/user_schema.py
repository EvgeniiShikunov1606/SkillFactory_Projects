USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "address"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {
            "type": "object",
            "required": ["street", "suite", "city", "zipcode", "get"],
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "required": ["lat", "lng"],
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"},
                    },
                },
            },
        },
    },
    "company": {
        "type": "object",
        "required": ["name", "catchPhrase", "bs"],
        "properties": {
            "name": {"type": "string"},
            "catchPhrase": {"type": "string"},
            "bs": {"type": "string"}
        },
    },
    "additionalProperties": False,
}
