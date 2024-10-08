policy1 = {
    "name": "Policy1",
    "schema_version": 1,
    "priority": 0,
    "enabled": True,
    "requires_approval": True,
    "conditions": {
        "logic": "parameter1.targets.name > parameter1.value1 AND parameter2.targets.name < parameter2.value1",
        "parameter1": {
            "targets": "Device",
            "name": "Bandwidth",
            "unit": "Mbps",
            "value1": "5"
        },
        "parameter2": {
            "targets": "Device",
            "name": "Temperature",
            "unit": "Celsius",
            "value1": "30"
        }
    },
    "actions": {
        "parameter1": {
            "targets": "Device",
            "name": "FanControl",
            "unit": "",
            "value": "ON"
        }
    }
}

policy2 = {
    "name": "Policy2",
    "schema_version": 1,
    "priority": 1,
    "enabled": True,
    "requires_approval": True,
    "conditions": {
        "logic": "parameter1.targets.name <= parameter1.value1 OR parameter2.targets.name >= parameter2.value1",
        "parameter1": {
            "targets": "Device",
            "name": "Bandwidth",
            "unit": "Mbps",
            "value1": "5"
        },
        "parameter2": {
            "targets": "Device",
            "name": "Temperature",
            "unit": "Celsius",
            "value1": "25"
        }
    },
    "actions": {
        "parameter1": {
            "targets": "Device",
            "name": "FanControl",
            "unit": "",
            "value": "OFF"
        }
    }
}

policy3 = {
    "name": "Policy3",
    "schema_version": 1,
    "priority": 2,
    "enabled": True,
    "requires_approval": True,
    "conditions": {
        "logic": "parameter1.targets.name > parameter1.value1 AND parameter2.targets.name < parameter2.value1",
        "parameter1": {
            "targets": "Device",
            "name": "Bandwidth",
            "unit": "Mbps",
            "value1": "10"
        },
        "parameter2": {
            "targets": "Device",
            "name": "Temperature",
            "unit": "Celsius",
            "value1": "20"
        }
    },
    "actions": {
        "parameter1": {
            "targets": "Device",
            "name": "CoolerControl",
            "unit": "",
            "value": "ON"
        }
    }
}

policy4 = {
    "name": "Policy4",
    "schema_version": 1,
    "priority": 3,
    "enabled": True,
    "requires_approval": True,
    "conditions": {
        "logic": "parameter1.targets.name < parameter1.value1 AND parameter2.targets.name >= parameter2.value1",
        "parameter1": {
            "targets": "Device",
            "name": "Bandwidth",
            "unit": "Mbps",
            "value1": "15"
        },
        "parameter2": {
            "targets": "Device",
            "name": "Temperature",
            "unit": "Celsius",
            "value1": "30"
        }
    },
    "actions": {
        "parameter1": {
            "targets": "Device",
            "name": "CoolerControl",
            "unit": "",
            "value": "OFF"
        }
    }
}

policy5 = {
    "name": "Policy5",
    "schema_version": 1,
    "priority": 4,
    "enabled": True,
    "requires_approval": True,
    "conditions": {
        "logic": "parameter1.targets.name <= parameter1.value1 AND parameter2.targets.name >= parameter2.value1",
        "parameter1": {
            "targets": "Device",
            "name": "Bandwidth",
            "unit": "Mbps",
            "value1": "10"
        },
        "parameter2": {
            "targets": "Device",
            "name": "Temperature",
            "unit": "Celsius",
            "value1": "20"
        }
    },
    "actions": {
        "parameter1": {
            "targets": "Device",
            "name": "FanControl",
            "unit": "",
            "value": "OFF"
        }
    }
}


from z3 import *

# Function to parse conditions and build a combined Z3 expression
def parse_conditions(policy):
    try:
        # Initialize a dictionary to hold dynamically created Z3 variables
        z3_vars = {}

        # Go through each parameter and dynamically create a Z3 variable based on targets and name
        for param_key, param_data in policy["conditions"].items():
            if param_key.startswith("parameter") and "targets" in param_data and "name" in param_data:
                # Dynamic variable name based on "targets" and "name"
                var_name = f"{param_data['targets']}.{param_data['name']}"
                
                # Create a Real Z3 variable dynamically
                z3_vars[var_name] = Real(var_name)
        
        # Extract value1 as floats from parameters
        parameter1_value1 = float(policy["conditions"]["parameter1"]["value1"])
        parameter2_value1 = float(policy["conditions"]["parameter2"]["value1"])

        # Initialize expression list
        exprs = []

        # Parse logic field and add to expressions dynamically based on variable names
        logic = policy["conditions"]["logic"]
        
        # For parameter1
        if "parameter1.targets.name > parameter1.value1" in logic:
            exprs.append(z3_vars["Device.Bandwidth"] > parameter1_value1)
        if "parameter1.targets.name <= parameter1.value1" in logic:
            exprs.append(z3_vars["Device.Bandwidth"] <= parameter1_value1)
        
        # For parameter2
        if "parameter2.targets.name < parameter2.value1" in logic:
            exprs.append(z3_vars["Device.Temperature"] < parameter2_value1)
        if "parameter2.targets.name >= parameter2.value1" in logic:
            exprs.append(z3_vars["Device.Temperature"] >= parameter2_value1)

        # Combine expressions with logical operators in the string
        if "AND" in logic:
            return And(*exprs)
        elif "OR" in logic:
            return Or(*exprs)
        else:
            return And(*exprs)
    except Exception as e:
        print(f"Error parsing conditions for policy '{policy['name']}': {e}")
        return None



def check_policy_conflict(policy1, policy2):
    try:
        s = Solver()
        cond1 = parse_conditions(policy1)
        cond2 = parse_conditions(policy2)

        # Check if conditions are parsed correctly (not None)
        if cond1 is not None and cond2 is not None:
            s.add(cond1)
            s.add(cond2)
            return s.check() == sat
        else:
            print(f"Skipping conflict check for {policy1['name']} and {policy2['name']} due to parsing error.")
            return False
    except Exception as e:
        print(f"Error checking conflict between '{policy1['name']}' and '{policy2['name']}': {e}")
        return False


# Main function with sample policies
# Main function with formatted output
def main():
    policies = [policy1, policy2, policy3, policy4, policy5]
    conflicts = []
    for i in range(len(policies)):
        for j in range(i + 1, len(policies)):
            if check_policy_conflict(policies[i], policies[j]):
                conflicts.append((policies[i]["name"], policies[j]["name"]))
    
    if conflicts:
        print("Conflicts detected:")
        for conflict in conflicts:
            print(f"{conflict[0]} and {conflict[1]}")
    else:
        print("No conflicts detected.")

if __name__ == "__main__":
    main()

