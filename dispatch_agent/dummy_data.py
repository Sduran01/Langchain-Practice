
company = {
    "company_id": 1,
    "name": "DA Transport",
    "dot_number": "1234567",
    "mc_number": "MC-123456",
    "headquarters": "Houston, TX",
    "phone": "555-010-2000",
    "email": "dispatch@datransport.example",
    "services": [
        "Full Truckload",
        "Regional Freight",
        "Long Haul"
    ]
}


drivers = {
    1: {
        "name": "John",
        "location": "Houston, TX",
        "truck": {
            "truck_number": "T101",
            "make": "Freightliner",
            "model": "Cascadia",
            "year": 2022,
            "max_cargo_payload_lbs": 48000
        },
        "trailer": {
            "trailer_number": "TR201",
            "type": "flatbed",
            "length_ft": 48
        }
    },
    2: {
        "name": "Carlos",
        "location": "Dallas, TX",
        "truck": {
            "truck_number": "T102",
            "make": "Kenworth",
            "model": "T680",
            "year": 2021,
            "max_cargo_payload_lbs": 45000
        },
        "trailer": {
            "trailer_number": "TR202",
            "type": "dry_van",
            "length_ft": 53
        }
    },
    3: {
        "name": "Mike",
        "location": "Austin, TX",
        "truck": {
            "truck_number": "T103",
            "make": "Peterbilt",
            "model": "579",
            "year": 2023,
            "max_cargo_payload_lbs": 46000
        },
        "trailer": {
            "trailer_number": "TR203",
            "type": "step_deck",
            "length_ft": 48
        }
    },
    4: {
        "name": "David",
        "location": "San Antonio, TX",
        "truck": {
            "truck_number": "T104",
            "make": "Volvo",
            "model": "VNL",
            "year": 2020,
            "max_cargo_payload_lbs": 44000
        },
        "trailer": {
            "trailer_number": "TR204",
            "type": "flatbed",
            "length_ft": 48
        }
    },
    5: {
        "name": "Jose",
        "location": "El Paso, TX",
        "truck": {
            "truck_number": "T105",
            "make": "International",
            "model": "LT",
            "year": 2022,
            "max_cargo_payload_lbs": 47000
        },
        "trailer": {
            "trailer_number": "TR205",
            "type": "reefer",
            "length_ft": 53
        }
    }
}


loads = {
    101: {
        "driver_id": 1,
        "pickup": "Houston, TX",
        "delivery": "Dallas, TX",
        "status": "in_transit",
        "cargo_weight_lbs": 42000,
        "required_trailer_type": "flatbed"
    },
    102: {
        "driver_id": 2,
        "pickup": "Dallas, TX",
        "delivery": "Austin, TX",
        "status": "delivered",
        "cargo_weight_lbs": 38000,
        "required_trailer_type": "dry_van"
    },
    103: {
        "driver_id": 3,
        "pickup": "Austin, TX",
        "delivery": "Houston, TX",
        "status": "assigned",
        "cargo_weight_lbs": 40000,
        "required_trailer_type": "step_deck"
    },
    104: {
        "driver_id": None,
        "pickup": "Houston, TX",
        "delivery": "San Antonio, TX",
        "status": "unassigned",
        "cargo_weight_lbs": 42000,
        "required_trailer_type": "dry_van"
    },
    105: {
        "driver_id": 1,
        "pickup": "Dallas, TX",
        "delivery": "Fort Worth, TX",
        "status": "assigned",
        "cargo_weight_lbs": 30000,
        "required_trailer_type": "flatbed"
    },
    106: {
        "driver_id": 4,
        "pickup": "San Antonio, TX",
        "delivery": "El Paso, TX",
        "status": "in_transit",
        "cargo_weight_lbs": 41000,
        "required_trailer_type": "flatbed"
    },
    107: {
        "driver_id": 5,
        "pickup": "El Paso, TX",
        "delivery": "Phoenix, AZ",
        "status": "delivered",
        "cargo_weight_lbs": 39000,
        "required_trailer_type": "reefer"
    },
    108: {
        "driver_id": None,
        "pickup": "Austin, TX",
        "delivery": "Dallas, TX",
        "status": "cancelled",
        "cargo_weight_lbs": 35000,
        "required_trailer_type": "step_deck"
    }
}


ACTIVE_STATUSES = {"assigned", "in_transit"}
