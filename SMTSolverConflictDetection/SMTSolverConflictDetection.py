import json
import os
from z3 import *

# Load all policies from a specified directory
def load_policies(directory):
    policies = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r') as file:
                        policy = json.load(file)
                        policies.append(policy)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {filename}: {e}")
                except IOError as e:
                    print(f"Error reading file {filename}: {e}")
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")
    return policies

# Translate a single condition into a z3 expression
def parse_condition(condition):
    try:
        parameter = condition["parameter"]
        operator = condition["operator"]
        value = condition["value"]
        
        if operator == "==":
            return Real(parameter) == float(value)
        elif operator == "!=":
            return Real(parameter) != float(value)
        elif operator == ">=":
            return Real(parameter) >= float(value)
        elif operator == "<=":
            return Real(parameter) <= float(value)
        elif operator == ">":
            return Real(parameter) > float(value)
        elif operator == "<":
            return Real(parameter) < float(value)
        else:
            raise ValueError(f"Unsupported operator '{operator}' in condition.")
    except KeyError as e:
        print(f"Missing key in condition: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing condition: {e}")
        return None

# Recursively parse nested conditions
def parse_conditions(conditions):
    try:
        logic = conditions.get("logic")
        if logic:
            sub_conditions = [parse_conditions(cond) for cond in conditions["conditions"]]
            sub_conditions = [cond for cond in sub_conditions if cond is not None]
            
            if logic == "AND":
                return And(*sub_conditions)
            elif logic == "OR":
                return Or(*sub_conditions)
            else:
                raise ValueError(f"Unsupported logic operator '{logic}' in conditions.")
        else:
            return parse_condition(conditions)
    except ValueError as e:
        print(f"Error parsing conditions: {e}")
        return None

# Check for conflicts among policies
def check_conflicts(policies):
    solver = Solver()
    for i, policy_a in enumerate(policies):
        for j, policy_b in enumerate(policies):
            if i >= j:
                continue  # Skip duplicates and self-comparisons
            
            try:
                # Reset the solver for each pair of policies
                solver.reset()
                
                # Parse and add conditions for both policies to the solver
                conditions_a = parse_conditions(policy_a["conditions"][0])
                conditions_b = parse_conditions(policy_b["conditions"][0])
                
                if conditions_a is None or conditions_b is None:
                    print(f"Skipping conflict check between Policy {policy_a['name']} and Policy {policy_b['name']} due to parsing issues.")
                    continue
                
                solver.add(And(conditions_a, conditions_b))
                
                # Check if both policies can be true at the same time
                if solver.check() == sat:
                    print(f"Conflict detected between Policy {policy_a['name']} and Policy {policy_b['name']}")
                else:
                    print(f"No conflict between Policy {policy_a['name']} and Policy {policy_b['name']}")
            
            except Exception as e:
                print(f"Error checking conflict between Policy {policy_a['name']} and Policy {policy_b['name']}: {e}")

# Main function to load policies and check for conflicts
def main():
    policy_directory = './ImprovedPolicy/'  # Replace with the actual directory path
    policies = load_policies(policy_directory)
    
    if policies:
        check_conflicts(policies)
    else:
        print("No valid policies were loaded.")

# Run the main function
if __name__ == "__main__":
    main()
