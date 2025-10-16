# import os
# import json
# import matplotlib.pyplot as plt
# import numpy as np
# from collections import defaultdict

# # Define paths
# BASE_DIR = os.path.dirname(__file__)
# OUTPUT_JSON_PATH = os.path.join(BASE_DIR, '../outputs/output.json')
# PLOTS_FOLDER = os.path.join(BASE_DIR, '../plots')
# os.makedirs(PLOTS_FOLDER, exist_ok=True)

# # Step 1: Parse output.json to get attribute values and assigned values
# with open(OUTPUT_JSON_PATH, 'r') as f:
#     output_data = json.load(f)

# SA_values = output_data["SAV"]
# OA_values = output_data["OAV"]
# EA_values = output_data["EAV"]
# SV = output_data["SV"]
# OV = output_data["OV"]
# EV = output_data["EV"]

# # Step 2: Count occurrences of each attribute value
# def count_occurrences(assigned_values):
#     counts = defaultdict(int)
#     for entity, attributes in assigned_values.items():
#         for value in attributes:
#             counts[value] += 1
#     return counts

# SA_counts = count_occurrences(SV)
# OA_counts = count_occurrences(OV)
# EA_counts = count_occurrences(EV)

# # Step 3: Calculate expected counts based on weights
# def calculate_expected_counts(attribute_values, assigned_values):
#     expected_counts = {}
#     total_assignments = len(assigned_values)  # Total number of entities assigned values
#     for key, values in attribute_values.items():
#         n = len(values)
#         weights = [2 ** (n - i - 1) for i in range(n)]  # Calculate weights
#         total_weight = sum(weights)
#         probabilities = [w / total_weight for w in weights]  # Normalize weights to probabilities
#         expected_counts[key] = {value: total_assignments * prob for value, prob in zip(values, probabilities)}
#     return expected_counts

# SA_expected_counts = calculate_expected_counts(SA_values, SV)
# OA_expected_counts = calculate_expected_counts(OA_values, OV)
# EA_expected_counts = calculate_expected_counts(EA_values, EV)

# # Step 4: Generate plots for each attribute
# def generate_plots(attribute_values, expected_counts, actual_counts, prefix):
#     for attribute, values in attribute_values.items():
#         # Get expected counts and actual counts
#         expected = [expected_counts[attribute][value] for value in values]
#         actual = [actual_counts[value] for value in values]

#         # Create the plot
#         x = np.arange(len(values))
#         width = 0.35

#         plt.figure(figsize=(10, 6))
#         plt.bar(x - width / 2, expected, width, label='Expected Count', color='blue')
#         plt.bar(x + width / 2, actual, width, label='Actual Count', color='orange')

#         # Add labels, title, and legend
#         plt.xlabel('Attribute Values')
#         plt.ylabel('Count')
#         plt.title(f'Expected vs Actual Count for {attribute}')
#         plt.xticks(x, values, rotation=45)
#         plt.legend()

#         # Save the plot
#         plot_path = os.path.join(PLOTS_FOLDER, f'{prefix}_{attribute}.png')
#         plt.tight_layout()
#         plt.savefig(plot_path)
#         plt.close()

# # Generate plots for subjects, objects, and environments
# generate_plots(SA_values, SA_expected_counts, SA_counts, "SA")
# generate_plots(OA_values, OA_expected_counts, OA_counts, "OA")
# generate_plots(EA_values, EA_expected_counts, EA_counts, "EA")

# print(f"Plots saved in {PLOTS_FOLDER}")


#################################################################



# import os
# import json
# import configparser
# import matplotlib.pyplot as plt
# import numpy as np
# import math  # Use math.factorial instead of np.math.factorial
# from collections import defaultdict

# # Define paths
# BASE_DIR = os.path.dirname(__file__)
# OUTPUT_JSON_PATH = os.path.join(BASE_DIR, '../outputs/output.json')
# CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')
# PLOTS_FOLDER = os.path.join(BASE_DIR, '../plots')
# os.makedirs(PLOTS_FOLDER, exist_ok=True)

# # Step 1: Parse config.ini to get attribute distributions and values
# config = configparser.ConfigParser()
# config.read(CONFIG_PATH)

# def parse_attributes(section):
#     return {
#         "count": int(config[section]["count"]),
#         "values": list(map(int, config[section]["values"].split(','))),
#         "distributions": json.loads(config[section]["distributions"])
#     }

# subject_attributes = parse_attributes("SUBJECT_ATTRIBUTES")
# object_attributes = parse_attributes("OBJECT_ATTRIBUTES")
# environment_attributes = parse_attributes("ENVIRONMENT_ATTRIBUTES")

# # Step 2: Parse output.json to get assigned values
# with open(OUTPUT_JSON_PATH, 'r') as f:
#     output_data = json.load(f)

# SA_values = output_data["SAV"]
# OA_values = output_data["OAV"]
# EA_values = output_data["EAV"]
# SV = output_data["SV"]
# OV = output_data["OV"]
# EV = output_data["EV"]

# # Step 3: Count occurrences of each attribute value
# def count_occurrences(assigned_values):
#     counts = defaultdict(int)
#     for entity, attributes in assigned_values.items():
#         for value in attributes:
#             counts[value] += 1
#     return counts

# SA_counts = count_occurrences(SV)
# OA_counts = count_occurrences(OV)
# EA_counts = count_occurrences(EV)

# # Step 4: Calculate expected counts based on distributions from config.ini
# def calculate_expected_counts(attribute_values, assigned_values, distributions):
#     expected_counts = defaultdict(float)
#     total_assignments = len(assigned_values)  # Total number of entities assigned values
#     for i, (key, values) in enumerate(attribute_values.items()):
#         dist = distributions[i]  # Get the distribution for the current attribute
#         n = len(values)
#         if dist["distribution"] == "N":
#             # Normal distribution
#             # mean = dist["mean"]
#             mean=0.5
#             # variance = dist["variance"]
#             variance=0.01
#             weights = [np.exp(-((j - mean) ** 2) / (2 * variance)) for j in range(1, n + 1)]
#         elif dist["distribution"] == "P":
#             # Poisson distribution
#             # lam = dist["lambda"]
#             lam=(1+n)/2.0

#             weights = [((lam ** j) * np.exp(-lam)) / math.factorial(j) for j in range(1, n + 1)]
#         else:
#             raise ValueError(f"Unsupported distribution type: {dist['distribution']}")

#         # Normalize weights to probabilities
#         total_weight = sum(weights)
#         probabilities = [w / total_weight for w in weights]

#         # Calculate expected counts for each value
#         for value, prob in zip(values, probabilities):
#             expected_counts[value] = total_assignments * prob
#     return expected_counts

# # Calculate expected counts for subjects, objects, and environments
# SA_expected_counts = calculate_expected_counts(SA_values, SV, subject_attributes["distributions"])
# OA_expected_counts = calculate_expected_counts(OA_values, OV, object_attributes["distributions"])
# EA_expected_counts = calculate_expected_counts(EA_values, EV, environment_attributes["distributions"])

# # Step 5: Generate plots for each attribute
# def generate_plots(attribute_values, expected_counts, actual_counts):
#     for attribute, values in attribute_values.items():
#         # Get expected counts and actual counts
#         expected = [expected_counts.get(value, 0) for value in values]
#         actual = [actual_counts.get(value, 0) for value in values]  # Use .get to handle missing values

#         # Create the plot
#         x = np.arange(len(values))
#         width = 0.35

#         plt.figure(figsize=(max(10, len(values) * 0.5), 6))  # Adjust figure size dynamically
#         plt.bar(x - width / 2, expected, width, label='Expected Count', color='blue')
#         plt.bar(x + width / 2, actual, width, label='Actual Count', color='orange')

#         # Add labels, title, and legend
#         plt.xlabel('Attribute Values')
#         plt.ylabel('Count')
#         plt.title(f'Expected vs Actual Count for {attribute}')
#         plt.xticks(x, values, rotation=45, ha='right')  # Rotate x-axis labels for readability
#         plt.legend()

#         # Save the plot
#         plot_path = os.path.join(PLOTS_FOLDER, f'{attribute}.png')
#         plt.tight_layout()
#         plt.savefig(plot_path)
#         plt.close()

# # Generate plots for subjects, objects, and environments
# generate_plots(SA_values, SA_expected_counts, SA_counts)
# generate_plots(OA_values, OA_expected_counts, OA_counts)
# generate_plots(EA_values, EA_expected_counts, EA_counts)

# print(f"Plots saved in {PLOTS_FOLDER}")



#################################################################


import os
import json
import configparser
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import defaultdict
from scipy.stats import norm

# --- Paths ---
BASE_DIR = os.path.dirname(__file__)
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, '../outputs/output.json')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')
PLOTS_FOLDER = os.path.join(BASE_DIR, '../plots')
os.makedirs(PLOTS_FOLDER, exist_ok=True)

# --- Read config ---
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

def parse_attributes(section):
    return {
        "count": int(config[section]["count"]),
        "values": list(map(int, config[section]["values"].split(','))),
        "distributions": json.loads(config[section]["distributions"])
    }

subject_attributes = parse_attributes("SUBJECT_ATTRIBUTES")
object_attributes = parse_attributes("OBJECT_ATTRIBUTES")
environment_attributes = parse_attributes("ENVIRONMENT_ATTRIBUTES")

# --- Read output.json ---
with open(OUTPUT_JSON_PATH, 'r') as f:
    output_data = json.load(f)

SA_values = output_data["SAV"]
OA_values = output_data["OAV"]
EA_values = output_data["EAV"]
SV = output_data["SV"]
OV = output_data["OV"]
EV = output_data["EV"]

# --- Count occurrences ---
def count_occurrences(assigned_values):
    counts = defaultdict(int)
    for entity, attributes in assigned_values.items():
        for value in attributes:
            counts[value] += 1
    return counts

SA_counts = count_occurrences(SV)
OA_counts = count_occurrences(OV)
EA_counts = count_occurrences(EV)

# --- Expected count calculation ---
def calculate_expected_counts(attribute_values, assigned_values, distributions):
    expected_counts = defaultdict(float)
    total_assignments = len(assigned_values)  # total entities for that type

    for i, (key, values) in enumerate(attribute_values.items()):
        dist = distributions[i]
        n = len(values)
        dist_type = dist["distribution"]

        if dist_type == "N":
            # Normal distribution with fixed mean and variance
            # mean = dist.get("mean", 0.5)
            mean=0.5
            # variance = dist.get("variance", 0.01)
            variance=0.01
            sigma = math.sqrt(variance)

            # Compute bin edges between 0 and 1
            edges = np.linspace(0, 1, n + 1)

            # Probability for each bin = area under PDF between edges
            probs = []
            for j in range(n):
                cdf_right = norm.cdf(edges[j + 1], loc=mean, scale=sigma)
                cdf_left = norm.cdf(edges[j], loc=mean, scale=sigma)
                probs.append(cdf_right - cdf_left)

        elif dist_type == "P":
            # Poisson distribution
            lam = dist["lambda"] # 
            weights = [((lam ** (j+1)) * math.exp(-lam)) / math.factorial(j+1) for j in range(n)]
            total_weight = sum(weights)
            probs = [w / total_weight for w in weights]

        elif dist_type == "U":
            # Uniform distribution
            probs = [1.0 / n] * n

        else:
            raise ValueError(f"Unsupported distribution type: {dist_type}")

        # Expected counts = probability * total assignments
        for value, prob in zip(values, probs):
            expected_counts[value] = total_assignments * prob

    return expected_counts

# --- Compute expected counts ---
SA_expected_counts = calculate_expected_counts(SA_values, SV, subject_attributes["distributions"])
OA_expected_counts = calculate_expected_counts(OA_values, OV, object_attributes["distributions"])
EA_expected_counts = calculate_expected_counts(EA_values, EV, environment_attributes["distributions"])

# --- Plotting ---

# def generate_plots(attribute_values, expected_counts, actual_counts):
#     for attribute, values in attribute_values.items():
#         expected = [expected_counts.get(value, 0) for value in values]
#         actual = [actual_counts.get(value, 0) for value in values]

#         x = np.arange(len(values))
#         width = 0.35

#         plt.figure(figsize=(max(10, len(values) * 0.5), 6))
#         plt.bar(x - width / 2, expected, width, label='Expected', color='blue')
#         plt.bar(x + width / 2, actual, width, label='Actual', color='orange')

#         plt.xlabel('Attribute Values')
#         plt.ylabel('Count')
#         plt.title(f'Expected vs Actual Count for {attribute}')
#         plt.xticks(x, values, rotation=45, ha='right')
#         plt.legend()

#         plot_path = os.path.join(PLOTS_FOLDER, f'{attribute}.png')
#         plt.tight_layout()
#         plt.savefig(plot_path)
#         plt.close()

def generate_plots(attribute_values, expected_counts, actual_counts):
    for attribute, values in attribute_values.items():
        expected = [expected_counts.get(value, 0) for value in values]
        actual = [actual_counts.get(value, 0) for value in values]

        x = np.arange(len(values))
        width = 0.35

        plt.figure(figsize=(max(10, len(values) * 0.5), 6))
        bars1 = plt.bar(x - width / 2, expected, width, label='Expected', color='blue')
        bars2 = plt.bar(x + width / 2, actual, width, label='Actual', color='orange')

        plt.xlabel('Attribute Values')
        plt.ylabel('Count')
        plt.title(f'Expected vs Actual Count for {attribute}')
        plt.xticks(x, values, rotation=45, ha='right')
        plt.legend()

        # --- Annotate counts above bars ---
        def annotate_bars(bars):
            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f'{int(height)}',          # or f'{height:.1f}' for decimals
                    ha='center',
                    va='bottom',
                    fontsize=9
                )

        annotate_bars(bars1)
        annotate_bars(bars2)

        plot_path = os.path.join(PLOTS_FOLDER, f'{attribute}.png')
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()


# --- Generate plots ---
generate_plots(SA_values, SA_expected_counts, SA_counts)
generate_plots(OA_values, OA_expected_counts, OA_counts)
generate_plots(EA_values, EA_expected_counts, EA_counts)

print(f" Plots saved in {PLOTS_FOLDER}")
