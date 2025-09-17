import random

# ********** WEIGHTED FUNCTIONS ARE INCOMPLETE **********

def generate_rules_1(N, n4, n5, n6, SA_values, OA_values, EA_values):
    rules = []
    
    for _ in range(N):
        rule_parts = []
        
        # Generate SA attributes
        for i in range(1, n4 + 1):
            key = f"SA_{i}"
            choices = SA_values.get(key, []) + ['*']
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate OA attributes
        for i in range(1, n5 + 1):
            key = f"OA_{i}"
            choices = OA_values.get(key, []) + ['*']
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate EA attributes
        for i in range(1, n6 + 1):
            key = f"EA_{i}"
            choices = EA_values.get(key, []) + ['*']
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        rules.append(", ".join(rule_parts))
        # print(rule_parts)
    
    return rules

def generate_rules_2(N, n4, n5, n6, SA_values, OA_values, EA_values):
    rules = []
    
    for _ in range(N):
        rule_parts = []
        
        # Generate SA attributes
        for i in range(1, n4 + 1):
            key = f"SA_{i}"
            choices = SA_values.get(key, []) + ['*', '*']  # Double the probability of '*'
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate OA attributes
        for i in range(1, n5 + 1):
            key = f"OA_{i}"
            choices = OA_values.get(key, []) + ['*', '*']  # Double the probability of '*'
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        # Generate EA attributes
        for i in range(1, n6 + 1):
            key = f"EA_{i}"
            choices = EA_values.get(key, []) + ['*', '*']  # Double the probability of '*'
            rule_parts.append(f"{key} = {random.choice(choices)}")
        
        rules.append(", ".join(rule_parts))
    
    return rules

def generate_rules_half(N, n4, n5, n6, SA_values, OA_values, EA_values):
    rules = []
    
    for _ in range(N):
        rule_parts = []
        
        # Function to choose with 50% probability for '*'
        def choose_value(values):
            if random.random() < 0.5:  # 50% probability of choosing '*'
                return '*'
            return random.choice(values) if values else '*'

        # Generate SA attributes
        for i in range(1, n4 + 1):
            key = f"SA_{i}"
            rule_parts.append(f"{key} = {choose_value(SA_values.get(key, []))}")
        
        # Generate OA attributes
        for i in range(1, n5 + 1):
            key = f"OA_{i}"
            rule_parts.append(f"{key} = {choose_value(OA_values.get(key, []))}")
        
        # Generate EA attributes
        for i in range(1, n6 + 1):
            key = f"EA_{i}"
            rule_parts.append(f"{key} = {choose_value(EA_values.get(key, []))}")
        
        rules.append(", ".join(rule_parts))
    
    return rules

def flatten_and_compute_weights(matrix):
    value_counts = {}
    total_count = 0

    for row in matrix:
        for value in row:
            value_counts[value] = value_counts.get(value, 0) + 1
            total_count += 1

    # Convert counts to probabilities
    weighted_values = list(value_counts.keys())
    weights = [count / total_count for count in value_counts.values()]

    print("Values and their probabilities:")
    for val, weight in zip(weighted_values, weights):
        print(f"{val}: {weight:.4f}")

    return weighted_values, weights

def generate_rules_weighted(N, n4, n5, n6, SV, OV, EV):
    rules = []

    # Compute weighted value distributions
    SA_values_, SA_weights_ = flatten_and_compute_weights(SV)
    OA_values_, OA_weights_ = flatten_and_compute_weights(OV)
    EA_values_, EA_weights_ = flatten_and_compute_weights(EV)

    for _ in range(N):
        rule_parts = []

        # Function to sample a value based on weights with '*' having fixed probability
        def choose_weighted(values, weights, star_prob=0.5):
            return random.choices(values, weights=weights, k=1)[0]

        # Generate SA attributes
        for i in range(1, n4 + 1):
            rule_parts.append(f"SA_{i} = {choose_weighted(SA_values_, SA_weights_)}")

        # Generate OA attributes
        for i in range(1, n5 + 1):
            rule_parts.append(f"OA_{i} = {choose_weighted(OA_values_, OA_weights_)}")

        # Generate EA attributes
        for i in range(1, n6 + 1):
            rule_parts.append(f"EA_{i} = {choose_weighted(EA_values_, EA_weights_)}")

        rules.append(", ".join(rule_parts))

    return rules

def flatten_and_compute_weights_1(matrix, star_weight):
    value_counts = {}
    total_count = 0

    for row in matrix:
        for value in row:
            value_counts[value] = value_counts.get(value, 0) + 1
            total_count += 1

    # Add '*' to the value list with a custom weight
    value_counts['*'] = star_weight
    total_count += star_weight

    # Convert counts to probabilities
    weighted_values = list(value_counts.keys())
    weights = [count / total_count for count in value_counts.values()]

    return weighted_values, weights

def generate_rules_weighted_1(N, n4, n5, n6, SV, OV, EV, star_weight=1):
    rules = []

    # Compute weighted value distributions with star_weight
    SA_values_, SA_weights_ = flatten_and_compute_weights_1(SV, star_weight)
    OA_values_, OA_weights_ = flatten_and_compute_weights_1(OV, star_weight)
    EA_values_, EA_weights_ = flatten_and_compute_weights_1(EV, star_weight)

    for _ in range(N):
        rule_parts = []

        # Function to sample a value based on weights
        def choose_weighted(values, weights):
            return random.choices(values, weights=weights, k=1)[0]

        # Generate SA attributes
        for i in range(1, n4 + 1):
            rule_parts.append(f"SA_{i} = {choose_weighted(SA_values_, SA_weights_)}")

        # Generate OA attributes
        for i in range(1, n5 + 1):
            rule_parts.append(f"OA_{i} = {choose_weighted(OA_values_, OA_weights_)}")

        # Generate EA attributes
        for i in range(1, n6 + 1):
            rule_parts.append(f"EA_{i} = {choose_weighted(EA_values_, EA_weights_)}")

        rules.append(", ".join(rule_parts))

    return rules

def generate_rules_weighted_half(N, n4, n5, n6, SV, OV, EV):
    rules = []

    # Compute weighted value distributions
    SA_values_, SA_weights_ = flatten_and_compute_weights(SV)
    OA_values_, OA_weights_ = flatten_and_compute_weights(OV)
    EA_values_, EA_weights_ = flatten_and_compute_weights(EV)

    for _ in range(N):
        rule_parts = []

        # Function to sample a value based on weights with '*' having fixed probability
        def choose_weighted(values, weights, star_prob=0.5):
            if random.random() < star_prob:
                return '*'
            return random.choices(values, weights=weights, k=1)[0]

        # Generate SA attributes
        for i in range(1, n4 + 1):
            rule_parts.append(f"SA_{i} = {choose_weighted(SA_values_, SA_weights_)}")

        # Generate OA attributes
        for i in range(1, n5 + 1):
            rule_parts.append(f"OA_{i} = {choose_weighted(OA_values_, OA_weights_)}")

        # Generate EA attributes
        for i in range(1, n6 + 1):
            rule_parts.append(f"EA_{i} = {choose_weighted(EA_values_, EA_weights_)}")

        rules.append(", ".join(rule_parts))

    return rules
