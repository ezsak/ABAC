import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Define paths
BASE_DIR = os.path.dirname(__file__)
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, '../outputs/output.json')
PLOTS_FOLDER = os.path.join(BASE_DIR, '../plots')
os.makedirs(PLOTS_FOLDER, exist_ok=True)

# Step 1: Parse output.json to get attribute values and assigned values
with open(OUTPUT_JSON_PATH, 'r') as f:
    output_data = json.load(f)

SA_values = output_data["SAV"]
OA_values = output_data["OAV"]
EA_values = output_data["EAV"]
SV = output_data["SV"]
OV = output_data["OV"]
EV = output_data["EV"]

# Step 2: Count occurrences of each attribute value
def count_occurrences(assigned_values):
    counts = defaultdict(int)
    for entity, attributes in assigned_values.items():
        for value in attributes:
            counts[value] += 1
    return counts

SA_counts = count_occurrences(SV)
OA_counts = count_occurrences(OV)
EA_counts = count_occurrences(EV)

# Step 3: Calculate expected counts based on weights
def calculate_expected_counts(attribute_values, assigned_values):
    expected_counts = {}
    total_assignments = len(assigned_values)  # Total number of entities assigned values
    for key, values in attribute_values.items():
        n = len(values)
        weights = [2 ** (n - i - 1) for i in range(n)]  # Calculate weights
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]  # Normalize weights to probabilities
        expected_counts[key] = {value: total_assignments * prob for value, prob in zip(values, probabilities)}
    return expected_counts

SA_expected_counts = calculate_expected_counts(SA_values, SV)
OA_expected_counts = calculate_expected_counts(OA_values, OV)
EA_expected_counts = calculate_expected_counts(EA_values, EV)

# Step 4: Generate plots for each attribute
def generate_plots(attribute_values, expected_counts, actual_counts, prefix):
    for attribute, values in attribute_values.items():
        # Get expected counts and actual counts
        expected = [expected_counts[attribute][value] for value in values]
        actual = [actual_counts[value] for value in values]

        # Create the plot
        x = np.arange(len(values))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x - width / 2, expected, width, label='Expected Count', color='blue')
        plt.bar(x + width / 2, actual, width, label='Actual Count', color='orange')

        # Add labels, title, and legend
        plt.xlabel('Attribute Values')
        plt.ylabel('Count')
        plt.title(f'Expected vs Actual Count for {attribute}')
        plt.xticks(x, values, rotation=45)
        plt.legend()

        # Save the plot
        plot_path = os.path.join(PLOTS_FOLDER, f'{prefix}_{attribute}.png')
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

# Generate plots for subjects, objects, and environments
generate_plots(SA_values, SA_expected_counts, SA_counts, "SA")
generate_plots(OA_values, OA_expected_counts, OA_counts, "OA")
generate_plots(EA_values, EA_expected_counts, EA_counts, "EA")

print(f"Plots saved in {PLOTS_FOLDER}")