from langchain_core.tools import tool
from dispatch_agent.dummy_data import (
    drivers,
    loads,
    ACTIVE_STATUSES,
)


@tool
def get_driver_active_loads(driver_id: int) -> dict:
    """Get a driver's active loads using their driver ID.

    Active loads have status 'assigned' or 'in_transit'.
    Delivered and cancelled loads are excluded.
    """
    if driver_id not in drivers:
        return {"error": "Driver not found"}

    active_loads = {
        load_id: load
        for load_id, load in loads.items()
        if load["driver_id"] == driver_id
        and load["status"] in ACTIVE_STATUSES
    }

    return {
        "driver_id": driver_id,
        "active_load_ids": list(active_loads.keys()),
        "active_loads": active_loads,
    }

@tool
def get_driver_availability(driver_id: int) -> dict:
    """Check whether a driver is currently available or busy.

    A driver is busy if they have at least one assigned
    or in-transit load. Otherwise they are available.
    This does not verify future scheduling or duty hours.
    """
    if driver_id not in drivers:
        return {"error": "Driver not found"}

    active_load_ids = [
        load_id
        for load_id, load in loads.items()
        if load["driver_id"] == driver_id
        and load["status"] in ACTIVE_STATUSES
    ]

    return {
        "driver_id": driver_id,
        "availability": "busy" if active_load_ids else "available",
        "active_load_ids": active_load_ids,
    }

@tool
def get_driver_location(driver_id: int) -> dict:
    """Get a driver's current known location by driver ID."""
    driver = drivers.get(driver_id)

    if driver is None:
        return {"error": "Driver not found"}

    return {
        "driver_id": driver_id,
        "driver_name": driver["name"],
        "location": driver["location"],
    }


@tool
def get_driver_equipment(driver_id: int) -> dict:
    """Get a driver's assigned truck and trailer information.

    Includes trailer type, trailer number, and maximum
    cargo payload capacity in pounds.
    """
    driver = drivers.get(driver_id)

    if driver is None:
        return {"error": "Driver not found"}

    return {
        "driver_id": driver_id,
        "driver_name": driver["name"],
        "truck": driver["truck"],
        "trailer": driver["trailer"],
    }


@tool
def get_load_details(load_id: int) -> dict:
    """Get load details, including status, route, cargo
    weight, trailer requirements, and assigned driver.
    """
    load = loads.get(load_id)

    if load is None:
        return {"error": "Load not found"}

    driver_id = load["driver_id"]
    driver = drivers.get(driver_id) if driver_id is not None else None

    return {
        "load_id": load_id,
        **load,
        "driver_name": driver["name"] if driver else None,
    }
tools = [
    get_driver_availability,
    get_driver_active_loads,
    get_driver_location,
    get_driver_equipment,
    get_load_details,
]