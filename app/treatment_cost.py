# Example treatment cost data (this could be connected to a real database or API)
treatment_costs = {
    "Cardiac Surgery": 15000,     # Example: Cardiac surgery cost estimate
    "Hip Replacement": 12000,     # Example: Hip replacement surgery cost estimate
    "Knee Replacement": 10000,    # Example: Knee replacement cost estimate
    "Cancer Treatment": 25000,    # Example: Cancer treatment cost estimate
    "Pediatric Care": 5000,       # Example: Pediatric care cost estimate
    "General Checkup": 200,       # Example: General health checkup cost estimate
}

def get_treatment_cost(disease):
    """
    Fetches the treatment cost from a predefined dictionary.
    
    :param disease: The disease or treatment type for which the cost is needed.
    :return: Estimated cost or a message indicating the cost is unavailable.
    """
    return treatment_costs.get(disease, "Cost estimate not available for this treatment.")

from app.mock_treatment_cost_api import get_mock_treatment_cost

def get_real_time_treatment_cost(disease_name, use_mock_api=True):
    """
    Fetches the real-time treatment cost. This function can switch between
    using the mock API or fetching from a real API if needed.
    
    :param disease_name: The name of the disease for which the treatment cost is required.
    :param use_mock_api: Flag to toggle between mock API and a real API.
    :return: Estimated treatment cost or an error message.
    """
    try:
        if use_mock_api:
            # Call the mock API to get the treatment cost
            return get_mock_treatment_cost(disease_name)
        else:
            # Example for real API integration (this can be replaced by actual API integration logic)
            # Make a real API call here, e.g., using `requests` or another library.
            # If you have a real endpoint, you would add the code to call that API.
            response = requests.get(f"https://real-api.com/treatment/{disease_name}")
            response.raise_for_status()  # Raise an exception if the API request fails
            return response.json().get("cost", "Cost data not available.")
    except requests.exceptions.RequestException as e:
        return f"Error fetching data from API: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# Example usage
disease_name = "Cancer Treatment"
print("Static Treatment Cost:", get_treatment_cost(disease_name))  # From the static dictionary
print("Real-Time Treatment Cost:", get_real_time_treatment_cost(disease_name))  # From the mock API or real API
