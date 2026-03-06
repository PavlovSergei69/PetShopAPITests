PET_SCHEMA = {
    "type": "object",
    "properties": { # характеритсики объекта. Смотреть пдф-лекцию
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "category": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                }
            },
            "required": ["id", "name"], # обязательные поля
            "additionalProperties": False # никаких дополнительных данных не должно быть
        },
        "photoUrls": {
            "type": "array",
            "items": { # предметы массива. Смотреть пдф-лекцию
                "type": "string"
            }
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                    "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": ["id", "name"],
                "additionalProperties": False
            }
        },
        "status": {
            "type": "string",
            "enum": ["available", "pending", "sold"]
        }
    },
    "required": ["id", "name", "photoUrls", "tags", "status"],
    "additionalProperties": False
}
