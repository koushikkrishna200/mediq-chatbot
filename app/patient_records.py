import pandas as pd

# Initialize a dataframe to hold patient records (could also be a database in the future)
patient_data = pd.DataFrame(columns=["patient_id", "name", "age", "conditions"])

# Set patient_id as index for faster search
patient_data.set_index("patient_id", inplace=True)

# Example to add a new patient record
def add_patient(patient_id, name, age, conditions):
    global patient_data
    # Validate the input data
    if not isinstance(age, (int, float)) or age <= 0:
        return "Invalid age."
    
    if not isinstance(conditions, list):
        return "Conditions must be a list."

    # Create new record and add to DataFrame
    new_record = pd.DataFrame([{
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "conditions": conditions
    }])
    
    new_record.set_index("patient_id", inplace=True)
    
    # Concatenate the new record with the existing DataFrame
    patient_data = pd.concat([patient_data, new_record])
    return f"Patient {name} added successfully."

# Example to fetch a patient's record
def get_patient_record(patient_id):
    patient = patient_data.loc[patient_id] if patient_id in patient_data.index else None
    if patient is None:
        return "Patient not found."
    return patient.to_dict()

# Example usage
add_patient(1, "John Doe", 45, ["Diabetes", "Hypertension"])
add_patient(2, "Jane Smith", 34, ["Asthma"])
print(get_patient_record(1))
