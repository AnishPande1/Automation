from RPA.Robocorp.WorkItems import WorkItems

def fetch_workitems() -> dict:
    """
    Retrieves the input parameters required for the entire process.
    """
    work_item = {
        "search_term": "India politics",
        "number_of_months": 4
    }

    return work_item
