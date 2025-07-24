import random
import time

# Dictionary simulating treatment costs for diseases
DISEASE_COSTS = {
    "Cardiac Surgery": 25000,
    "Cancer Treatment": 40000,
    "Diabetes Management": 10000,
    "Hip Replacement": 15000,
    "Knee Surgery": 12000,
    "Stroke Rehabilitation": 20000,
    "Cancer Chemotherapy": 35000,
    "Spinal Surgery": 30000,
    "Brain Tumor Surgery": 50000,
    "Heart Attack Treatment": 22000
}

def get_mock_treatment_cost(disease_name):
    """
    Simulate an API call to get the treatment cost for a given disease.
    
    :param disease_name: Name of the disease to fetch treatment cost.
    :return: Estimated cost of treatment for the disease or error message if disease not found.
    """
    # Simulate API delay
    simulated_delay = random.uniform(0.5, 2.0)  # Random delay between 0.5 to 2 seconds
    time.sleep(simulated_delay)  # Simulate delay

    # Return the cost if the disease is found, else raise an exception
    if disease_name in DISEASE_COSTS:
        return DISEASE_COSTS[disease_name]
    else:
        raise ValueError(f"Cost for '{disease_name}' is not available. Please try another disease.")
