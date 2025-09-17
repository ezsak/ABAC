# import configparser
# import random
# import gen_rules
# import json
# import os

# # Ensure config.ini exists in the access_control directory
# config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
# if not os.path.exists(config_path):
#     raise FileNotFoundError("config.ini not found. Ensure input.py runs successfully before gen.py.")

# # Load the config file
# config = configparser.ConfigParser()
# config.read(config_path)

# # Define output directory inside flask_app/outputs
# OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../outputs')
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Read values from config.ini
# n1 = int(config["NUMBERS"]["n1"])
# n2 = int(config["NUMBERS"]["n2"])
# n3 = int(config["NUMBERS"]["n3"])
# n4 = int(config["NUMBERS"]["n4"])
# n5 = int(config["NUMBERS"]["n5"])
# n6 = int(config["NUMBERS"]["n6"])
# subject_attributes = list(map(int, config["SUBJECT_ATTRIBUTES"]["values"].split(',')))
# object_attributes = list(map(int, config["OBJECT_ATTRIBUTES"]["values"].split(',')))
# environment_attributes = list(map(int, config["ENVIRONMENT_ATTRIBUTES"]["values"].split(',')))
# N = int(config["RULES"]["N"])

# # Generate users, objects, and environments
# S = [f"S_{i}" for i in range(1, n1 + 1)]
# O = [f"O_{i}" for i in range(1, n2 + 1)]
# E = [f"E_{i}" for i in range(1, n3 + 1)]

# # Generate attribute names
# SA = [f"SA_{i}" for i in range(1, n4 + 1)]
# OA = [f"OA_{i}" for i in range(1, n5 + 1)]
# EA = [f"EA_{i}" for i in range(1, n6 + 1)]

# # Generate attribute values
# SA_values = {}
# for i, num_values in enumerate(subject_attributes, start=1):
#     SA_values[f"SA_{i}"] = [f"SA_{i}_{j}" for j in range(1, num_values + 1)]

# OA_values = {}
# for i, num_values in enumerate(object_attributes, start=1):
#     OA_values[f"OA_{i}"] = [f"OA_{i}_{j}" for j in range(1, num_values + 1)]

# EA_values = {}
# for i, num_values in enumerate(environment_attributes, start=1):
#     EA_values[f"EA_{i}"] = [f"EA_{i}_{j}" for j in range(1, num_values + 1)]

# # Generate random attribute values for subjects, objects, and environments
# SV = {S[i]: [random.choice(SA_values[SA[j]]) for j in range(n4)] for i in range(n1)}
# OV = {O[i]: [random.choice(OA_values[OA[j]]) for j in range(n5)] for i in range(n2)}
# EV = {E[i]: [random.choice(EA_values[EA[j]]) for j in range(n6)] for i in range(n3)}

# # Create output.json
# output_data = {
#     "S": S,
#     "O": O,
#     "E": E,
#     "SA": SA,
#     "OA": OA,
#     "EA": EA,
#     "SAV": SA_values,
#     "OAV": OA_values,
#     "EAV": EA_values,
#     "SV": SV,
#     "OV": OV,
#     "EV": EV
# }

# with open(os.path.join(OUTPUT_FOLDER, 'output.json'), 'w') as f:
#     json.dump(output_data, f, indent=4)

# # Generate rules and write to rules_temp.txt
# rules = gen_rules.generate_rules_2(N, n4, n5, n6, SA_values, OA_values, EA_values)

# with open(os.path.join(OUTPUT_FOLDER, "rules_temp.txt"), "w") as file:
#     for rule in rules:
#         file.write(rule + "\n")






# A = [[[0] * n3 for _ in range(n2)] for _ in range(n1)]

# no_of_ones = 0
# def satisfies_rule(rule, SA1, OA1, EA1):
#     rule_parts = rule.split(", ")
#     for part in rule_parts:
#         key, value = part.split(" = ")
#         if key.startswith("SA_") and value not in SA1 and value != '*':
#             return False
#         if key.startswith("OA_") and value not in OA1 and value != '*':
#             return False
#         if key.startswith("EA_") and value not in EA1 and value != '*':
#             return False
#     return True


# def fill_matrix(A, SV, OV, EV, rules, n1, n2, n3):
#     global no_of_ones
#     for i in range(n1):
#         for j in range(n2):
#             for k in range(n3):
#                 # Access SV, OV, and EV using subject, object, and environment names
#                 SA1 = SV[f"S_{i + 1}"]
#                 OA1 = OV[f"O_{j + 1}"]
#                 EA1 = EV[f"E_{k + 1}"]
                
#                 # Check if any rule is satisfied
#                 A[i][j][k] = 1 if any(satisfies_rule(rule, SA1, OA1, EA1) for rule in rules) else 0
#                 no_of_ones += A[i][j][k]

# fill_matrix(A, SV, OV, EV, rules, n1, n2, n3)
# print("No. of ones in ACM : ", no_of_ones)

# with open(os.path.join(OUTPUT_FOLDER, "ACM.txt"), "w") as file:
#     for i in range(n1):
#         for row in A[i]:
#             file.write(" ".join(map(str, row)) + "\n")
#         file.write("\n")


# def prepare_access_data(S, O, E, SV, OV, EV, A):
#     access_data = []
#     for i in range(len(S)):
#         for j in range(len(O)):
#             for k in range(len(E)):
#                 # Access SV, OV, and EV using subject, object, and environment names
#                 subject = S[i]
#                 obj = O[j]
#                 env = E[k]
#                 T = SV[subject] + OV[obj] + EV[env] + [A[i][j][k]]  # Concatenate attributes and access decision
#                 access_data.append(T)
#     return access_data
# access_data = prepare_access_data(S, O, E, SV, OV, EV, A)

# with open(os.path.join(OUTPUT_FOLDER, "access_data.txt"), "w") as file:
#     for row in access_data:
#         file.write(" ".join(map(str, row)) + "\n")


# import configparser
# import random
# import gen_rules
# import json
# import os

# # Ensure config.ini exists in the access_control directory
# config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
# if not os.path.exists(config_path):
#     raise FileNotFoundError("config.ini not found. Ensure input.py runs successfully before gen.py.")

# # Load the config file
# config = configparser.ConfigParser()
# config.read(config_path)

# # Define output directory inside flask_app/outputs
# OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../outputs')
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Read values from config.ini
# n1 = int(config["NUMBERS"]["n1"])
# n2 = int(config["NUMBERS"]["n2"])
# n3 = int(config["NUMBERS"]["n3"])
# n4 = int(config["NUMBERS"]["n4"])
# n5 = int(config["NUMBERS"]["n5"])
# n6 = int(config["NUMBERS"]["n6"])
# subject_attributes = list(map(int, config["SUBJECT_ATTRIBUTES"]["values"].split(',')))
# object_attributes = list(map(int, config["OBJECT_ATTRIBUTES"]["values"].split(',')))
# environment_attributes = list(map(int, config["ENVIRONMENT_ATTRIBUTES"]["values"].split(',')))
# N = int(config["RULES"]["N"])

# # Generate users, objects, and environments
# S = [f"S_{i}" for i in range(1, n1 + 1)]
# O = [f"O_{i}" for i in range(1, n2 + 1)]
# E = [f"E_{i}" for i in range(1, n3 + 1)]

# # Generate attribute names
# SA = [f"SA_{i}" for i in range(1, n4 + 1)]
# OA = [f"OA_{i}" for i in range(1, n5 + 1)]
# EA = [f"EA_{i}" for i in range(1, n6 + 1)]

# # Generate unique attribute values
# def generate_unique_values(attribute_count, num_values_list, prefix):
#     values = {}
#     used_values = set()  # To ensure global uniqueness of values
#     for i in range(1, attribute_count + 1):
#         attribute_values = []
#         while len(attribute_values) < num_values_list[i - 1]:
#             value = random.randint(1, 200)  # Uniform distribution between 1 and 200
#             if value not in used_values:
#                 attribute_values.append(f"{prefix}_{i}_{value}")
#                 used_values.add(value)
#         values[f"{prefix}_{i}"] = attribute_values
#     return values

# SA_values = generate_unique_values(n4, subject_attributes, "SA")
# OA_values = generate_unique_values(n5, object_attributes, "OA")
# EA_values = generate_unique_values(n6, environment_attributes, "EA")

# # Generate random attribute values for subjects, objects, and environments
# SV = {S[i]: [random.choice(SA_values[SA[j]]) for j in range(n4)] for i in range(n1)}
# OV = {O[i]: [random.choice(OA_values[OA[j]]) for j in range(n5)] for i in range(n2)}
# EV = {E[i]: [random.choice(EA_values[EA[j]]) for j in range(n6)] for i in range(n3)}

# # Create output.json
# output_data = {
#     "S": S,
#     "O": O,
#     "E": E,
#     "SA": SA,
#     "OA": OA,
#     "EA": EA,
#     "SAV": SA_values,
#     "OAV": OA_values,
#     "EAV": EA_values,
#     "SV": SV,
#     "OV": OV,
#     "EV": EV
# }

# with open(os.path.join(OUTPUT_FOLDER, 'output.json'), 'w') as f:
#     json.dump(output_data, f, indent=4)

# # Generate rules and write to rules_temp.txt
# rules = gen_rules.generate_rules_2(N, n4, n5, n6, SA_values, OA_values, EA_values)

# with open(os.path.join(OUTPUT_FOLDER, "rules_temp.txt"), "w") as file:
#     for rule in rules:
#         file.write(rule + "\n")

import configparser
import random
import gen_rules
import json
import os
import numpy as np

# Ensure config.ini exists in the access_control directory
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
if not os.path.exists(config_path):
    raise FileNotFoundError("config.ini not found. Ensure input.py runs successfully before gen.py.")

# Load the config file
config = configparser.ConfigParser()
config.read(config_path)

# Define output directory inside flask_app/outputs
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../outputs')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read values from config.ini
n1 = int(config["NUMBERS"]["n1"])
n2 = int(config["NUMBERS"]["n2"])
n3 = int(config["NUMBERS"]["n3"])
n4 = int(config["NUMBERS"]["n4"])
n5 = int(config["NUMBERS"]["n5"])
n6 = int(config["NUMBERS"]["n6"])
subject_attributes = list(map(int, config["SUBJECT_ATTRIBUTES"]["values"].split(',')))
object_attributes = list(map(int, config["OBJECT_ATTRIBUTES"]["values"].split(',')))
environment_attributes = list(map(int, config["ENVIRONMENT_ATTRIBUTES"]["values"].split(',')))
N = int(config["RULES"]["N"])

# Read mean and variance for Gaussian distribution from config.ini
subject_mean = float(config["GAUSSIAN"]["subject_mean"])
subject_variance = float(config["GAUSSIAN"]["subject_variance"])
object_mean = float(config["GAUSSIAN"]["object_mean"])
object_variance = float(config["GAUSSIAN"]["object_variance"])
environment_mean = float(config["GAUSSIAN"]["environment_mean"])
environment_variance = float(config["GAUSSIAN"]["environment_variance"])

# Generate users, objects, and environments
S = [f"S_{i}" for i in range(1, n1 + 1)]
O = [f"O_{i}" for i in range(1, n2 + 1)]
E = [f"E_{i}" for i in range(1, n3 + 1)]

# Generate attribute names
SA = [f"SA_{i}" for i in range(1, n4 + 1)]
OA = [f"OA_{i}" for i in range(1, n5 + 1)]
EA = [f"EA_{i}" for i in range(1, n6 + 1)]

# Generate unique attribute values
def generate_unique_values(attribute_count, num_values_list, prefix):
    values = {}
    used_values = set()  # To ensure global uniqueness of values
    for i in range(1, attribute_count + 1):
        attribute_values = []
        while len(attribute_values) < num_values_list[i - 1]:
            value = random.randint(1, 200)  # Uniform distribution between 1 and 200
            if value not in used_values:
                attribute_values.append(f"{prefix}_{i}_{value}")
                used_values.add(value)
        values[f"{prefix}_{i}"] = attribute_values
    return values

SA_values = generate_unique_values(n4, subject_attributes, "SA")
OA_values = generate_unique_values(n5, object_attributes, "OA")
EA_values = generate_unique_values(n6, environment_attributes, "EA")

# Assign attribute values to users, objects, and environments using Gaussian distribution
# Assign attribute values to users, objects, and environments using Gaussian distribution
# def assign_values_gaussian(attribute_values, entity_count, mean, variance, prefix):
#     """
#     Assign exactly one value for each attribute to entities (subjects, objects, or environments).
#     """
#     entity_values = {}
#     for entity in range(1, entity_count + 1):
#         entity_values[f"{prefix}_{entity}"] = [
#             random.choice(attribute_values[key])  # Pick exactly one value for each attribute
#             for key in attribute_values
#         ]
#     return entity_values

# Assign attribute values to users, objects, and environments using weighted probabilities
def assign_values_weighted(attribute_values, entity_count, prefix):
    """
    Assign exactly one value for each attribute to entities (subjects, objects, or environments),
    using a weighted probability distribution where the first value is twice as likely as the second,
    the second is twice as likely as the third, and so on.
    """
    entity_values = {}
    for entity in range(1, entity_count + 1):
        entity_values[f"{prefix}_{entity}"] = [
            random.choices(
                attribute_values[key],  # List of possible values for the attribute
                weights=[2 ** (len(attribute_values[key]) - i - 1) for i in range(len(attribute_values[key]))]
            )[0]  # Select one value based on the weights
            for key in attribute_values
        ]
    return entity_values

# Assign values to subjects, objects, and environments
SV = assign_values_weighted(SA_values, n1, "S")
OV = assign_values_weighted(OA_values, n2, "O")
EV = assign_values_weighted(EA_values, n3, "E")

# #Assign values to subjects, objects, and environments
# SV = assign_values_gaussian(SA_values, n1, subject_mean, subject_variance, "S")
# OV = assign_values_gaussian(OA_values, n2, object_mean, object_variance, "O")
# EV = assign_values_gaussian(EA_values, n3, environment_mean, environment_variance, "E")

# Create output.json
output_data = {
    "S": S,
    "O": O,
    "E": E,
    "SA": SA,
    "OA": OA,
    "EA": EA,
    "SAV": SA_values,
    "OAV": OA_values,
    "EAV": EA_values,
    "SV": SV,
    "OV": OV,
    "EV": EV
}

with open(os.path.join(OUTPUT_FOLDER, 'output.json'), 'w') as f:
    json.dump(output_data, f, indent=4)

# Generate rules and write to rules_temp.txt
rules = gen_rules.generate_rules_2(N, n4, n5, n6, SA_values, OA_values, EA_values)

with open(os.path.join(OUTPUT_FOLDER, "rules_temp.txt"), "w") as file:
    for rule in rules:
        file.write(rule + "\n")

# Initialize the Access Control Matrix (ACM)
A = [[[0] * n3 for _ in range(n2)] for _ in range(n1)]

no_of_ones = 0
def satisfies_rule(rule, SA1, OA1, EA1):
    rule_parts = rule.split(", ")
    for part in rule_parts:
        key, value = part.split(" = ")
        if key.startswith("SA_") and value not in SA1 and value != '*':
            return False
        if key.startswith("OA_") and value not in OA1 and value != '*':
            return False
        if key.startswith("EA_") and value not in EA1 and value != '*':
            return False
    return True

def fill_matrix(A, SV, OV, EV, rules, n1, n2, n3):
    global no_of_ones
    for i in range(n1):
        for j in range(n2):
            for k in range(n3):
                # Access SV, OV, and EV using subject, object, and environment names
                SA1 = SV[f"S_{i + 1}"]
                OA1 = OV[f"O_{j + 1}"]
                EA1 = EV[f"E_{k + 1}"]
                
                # Check if any rule is satisfied
                A[i][j][k] = 1 if any(satisfies_rule(rule, SA1, OA1, EA1) for rule in rules) else 0
                no_of_ones += A[i][j][k]

fill_matrix(A, SV, OV, EV, rules, n1, n2, n3)
print("No. of ones in ACM : ", no_of_ones)

# Write ACM to ACM.txt
with open(os.path.join(OUTPUT_FOLDER, "ACM.txt"), "w") as file:
    for i in range(n1):
        for row in A[i]:
            file.write(" ".join(map(str, row)) + "\n")
        file.write("\n")

# Prepare access_data.txt
def prepare_access_data(S, O, E, SV, OV, EV, A):
    access_data = []
    for i in range(len(S)):
        for j in range(len(O)):
            for k in range(len(E)):
                # Access SV, OV, and EV using subject, object, and environment names
                subject = S[i]
                obj = O[j]
                env = E[k]
                T = SV[subject] + OV[obj] + EV[env] + [A[i][j][k]]  # Concatenate attributes and access decision
                access_data.append(T)
    return access_data

access_data = prepare_access_data(S, O, E, SV, OV, EV, A)

with open(os.path.join(OUTPUT_FOLDER, "access_data.txt"), "w") as file:
    for row in access_data:
        file.write(" ".join(map(str, row)) + "\n")