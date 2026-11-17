
evaluation_data = [
    {
        "inputs": {
            "question": "Is John available, and what active loads does he have?"
        },
        "outputs": {
            "expected_tool_calls": [
                {
                    "name": "get_driver_availability",
                    "args": {"driver_id": 1}
                },
                {
                    "name": "get_driver_active_loads",
                    "args": {"driver_id": 1}
                }
            ],
            "expected_facts": {
                "availability": "busy",
                "active_load_ids": [101, 105]
            }
        }
    },
    {
        "inputs": {
            "question": "Can Carlos haul a 44,000 lb load requiring a dry van?"
        },
        "outputs": {
            "expected_tool_calls": [
                {
                    "name": "get_driver_equipment",
                    "args": {"driver_id": 2}
                }
            ],
            "expected_facts": {
                "trailer_type": "dry_van",
                "max_cargo_payload_lbs": 45000,
                "equipment_compatible": True
            }
        }
    },
    {
        "inputs": {
            "question": "What is the status of load 103, and who is assigned to it?"
        },
        "outputs": {
            "expected_tool_calls": [
                {
                    "name": "get_load_details",
                    "args": {"load_id": 103}
                }
            ],
            "expected_facts": {
                "status": "assigned",
                "driver_id": 3,
                "driver_name": "Mike"
            }
        }
    },
    {
        "inputs": {
            "question": "Which trailer does David have, and how much cargo can he haul?"
        },
        "outputs": {
            "expected_tool_calls": [
                {
                    "name": "get_driver_equipment",
                    "args": {"driver_id": 4}
                }
            ],
            "expected_facts": {
                "trailer_number": "TR204",
                "trailer_type": "flatbed",
                "max_cargo_payload_lbs": 44000
            }
        }
    },
    {
        "inputs": {
            "question": "Is Jose available, where is he, and what type of trailer does he have?"
        },
        "outputs": {
            "expected_tool_calls": [
                {
                    "name": "get_driver_availability",
                    "args": {"driver_id": 5}
                },
                {
                    "name": "get_driver_location",
                    "args": {"driver_id": 5}
                },
                {
                    "name": "get_driver_equipment",
                    "args": {"driver_id": 5}
                }
            ],
            "expected_facts": {
                "availability": "available",
                "location": "El Paso, TX",
                "trailer_type": "reefer"
            }
        }
    }
]