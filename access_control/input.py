# import configparser
# import json
# import os

# def write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N):
#     config = configparser.ConfigParser()
    
#     config['NUMBERS'] = {
#         'n1': str(n1), 'n2': str(n2), 'n3': str(n3),
#         'n4': str(n4), 'n5': str(n5), 'n6': str(n6)
#     }
    
#     config['SUBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, subject_attributes))}
#     config['OBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, object_attributes))}
#     config['ENVIRONMENT_ATTRIBUTES'] = {'values': ','.join(map(str, environment_attributes))}

#     config['RULES'] = {'N': str(N)}
    
#     # Write config.ini inside the access_control directory
#     config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
#     with open(config_path, 'w') as configfile:
#         config.write(configfile)

# def read_input_json(file_path):
#     with open(file_path, "r") as file:
#         data = json.load(file)
#         return data

# if __name__ == "__main__":
#     # Read input.json from the uploads directory
#     input_path = os.path.join(os.path.dirname(__file__), '../uploads/input.json')
#     input_data = read_input_json(input_path)
    
#     # Extract values from JSON
#     n1 = input_data["subject_size"]
#     n2 = input_data["object_size"]
#     n3 = input_data["environment_size"]
#     n4 = input_data["subject_attributes_count"]
#     n5 = input_data["object_attributes_count"]
#     n6 = input_data["environment_attributes_count"]
#     subject_attributes = input_data["subject_attributes_values"]
#     object_attributes = input_data["object_attributes_values"]
#     environment_attributes = input_data["environment_attributes_values"]
#     N = input_data["rules_count"]

#     # Write to config.ini
#     write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N)

# import configparser
# import json
# import os
# import random
# import numpy as np

# def write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N):
#     config = configparser.ConfigParser()
    
#     config['NUMBERS'] = {
#         'n1': str(n1), 'n2': str(n2), 'n3': str(n3),
#         'n4': str(n4), 'n5': str(n5), 'n6': str(n6)
#     }
    
#     config['SUBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, subject_attributes))}
#     config['OBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, object_attributes))}
#     config['ENVIRONMENT_ATTRIBUTES'] = {'values': ','.join(map(str, environment_attributes))}

#     config['RULES'] = {'N': str(N)}
    
#     # Write config.ini inside the access_control directory
#     config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
#     with open(config_path, 'w') as configfile:
#         config.write(configfile)

# def generate_attribute_values(attribute_count, mean, variance, value_range):
#     """
#     Generate attribute values based on Gaussian distribution.
#     """
#     values = {}
#     for i in range(1, attribute_count + 1):
#         num_values = max(1, int(np.random.normal(mean, variance)))  # Ensure at least 1 value
#         values[f"SA_{i}"] = [f"SA_{i}_{random.randint(*value_range)}" for _ in range(num_values)]
#     return values

# def assign_values_to_users(attribute_values, user_count, mean, variance):
#     """
#     Assign attribute values to users based on Gaussian distribution.
#     """
#     user_values = {}
#     for user in range(1, user_count + 1):
#         user_values[f"S_{user}"] = [
#             random.choices(values, k=max(1, int(np.random.normal(mean, variance))))
#             for values in attribute_values.values()
#         ]
#     return user_values

# def read_input_json(file_path):
#     with open(file_path, "r") as file:
#         data = json.load(file)
#         return data

# if __name__ == "__main__":
#     # Read input.json from the dataset directory
#     input_path = os.path.join(os.path.dirname(__file__), '../dataset/input.json')
#     input_data = read_input_json(input_path)
    
#     # Extract values from JSON
#     n1 = input_data["subject_size"]
#     n2 = input_data["object_size"]
#     n3 = input_data["environment_size"]
#     n4 = input_data["subject_attributes_count"]
#     n5 = input_data["object_attributes_count"]
#     n6 = input_data["environment_attributes_count"]
#     subject_mean = input_data["subject_mean"]
#     subject_variance = input_data["subject_variance"]
#     object_mean = input_data["object_mean"]
#     object_variance = input_data["object_variance"]
#     environment_mean = input_data["environment_mean"]
#     environment_variance = input_data["environment_variance"]
#     value_range = (1, 200)
#     N = input_data["rules_count"]

#     # Generate attribute values
#     subject_attributes = generate_attribute_values(n4, subject_mean, subject_variance, value_range)
#     object_attributes = generate_attribute_values(n5, object_mean, object_variance, value_range)
#     environment_attributes = generate_attribute_values(n6, environment_mean, environment_variance, value_range)

#     # Assign values to users, objects, and environments
#     subject_values = assign_values_to_users(subject_attributes, n1, subject_mean, subject_variance)
#     object_values = assign_values_to_users(object_attributes, n2, object_mean, object_variance)
#     environment_values = assign_values_to_users(environment_attributes, n3, environment_mean, environment_variance)

#     # Write to config.ini
#     write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N)

import configparser
import json
import os

def write_config_file(n1, n2, n3, n4, n5, n6, subject_attributes, object_attributes, environment_attributes, N, subject_mean, subject_variance, object_mean, object_variance, environment_mean, environment_variance):
    """
    Write the configuration to config.ini.
    """
    config = configparser.ConfigParser()
    
    # Write numbers
    config['NUMBERS'] = {
        'n1': str(n1), 'n2': str(n2), 'n3': str(n3),
        'n4': str(n4), 'n5': str(n5), 'n6': str(n6)
    }
    
    # Write attribute counts
    config['SUBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, subject_attributes))}
    config['OBJECT_ATTRIBUTES'] = {'values': ','.join(map(str, object_attributes))}
    config['ENVIRONMENT_ATTRIBUTES'] = {'values': ','.join(map(str, environment_attributes))}

    # Write rules count
    config['RULES'] = {'N': str(N)}

    # Write Gaussian distribution parameters
    config['GAUSSIAN'] = {
        'subject_mean': str(subject_mean),
        'subject_variance': str(subject_variance),
        'object_mean': str(object_mean),
        'object_variance': str(object_variance),
        'environment_mean': str(environment_mean),
        'environment_variance': str(environment_variance)
    }
    
    # Write config.ini inside the access_control directory
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def read_input_json(file_path):
    """
    Read input.json and return the parsed data.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
        return data

if __name__ == "__main__":
    # Read input.json from the dataset directory
    input_path = os.path.join(os.path.dirname(__file__), '../uploads/input.json')
    input_data = read_input_json(input_path)
    
    # Extract values from JSON
    n1 = input_data["subject_size"]
    n2 = input_data["object_size"]
    n3 = input_data["environment_size"]
    n4 = input_data["subject_attributes_count"]
    n5 = input_data["object_attributes_count"]
    n6 = input_data["environment_attributes_count"]
    subject_attributes = input_data["subject_attributes_values"]
    object_attributes = input_data["object_attributes_values"]
    environment_attributes = input_data["environment_attributes_values"]
    N = input_data["rules_count"]

    # Extract Gaussian distribution parameters
    subject_mean = input_data["subject_mean"]
    subject_variance = input_data["subject_variance"]
    object_mean = input_data["object_mean"]
    object_variance = input_data["object_variance"]
    environment_mean = input_data["environment_mean"]
    environment_variance = input_data["environment_variance"]

    # Write to config.ini
    write_config_file(
        n1, n2, n3, n4, n5, n6,
        subject_attributes, object_attributes, environment_attributes,
        N,
        subject_mean, subject_variance,
        object_mean, object_variance,
        environment_mean, environment_variance
    )