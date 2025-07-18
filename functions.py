import pandas as pd

# Load the main CSV (you'll need to save the relevant sheet as a CSV from Excel first)
main_df = pd.read_csv("DW14-PR-Personal Auto-UW-Rules_StateRollouts(Validation and UW Rules)")
left_out_df = pd.read_csv("Base_Rules_left_out_of_orig_DW.csv")

# Inspect columns
print("Main Columns:", main_df.columns.tolist())
print("Left-out Columns:", left_out_df.columns.tolist())

# Define which columns are state indicators (adjust based on your actual CSV headers)
state_columns = ['TX', 'OK', 'PA', 'WI', 'OHM', 'OH-FR', 'AZ', 'CA', 'NV', 'NM', 'UT', 'CO', 
                 'IN-M', 'IN-MD', 'IL-M', 'IL-MD']

# Filter for rows where all state values == "YES"
common_rules_df = main_df[main_df[state_columns].apply(lambda row: all(row == "YES"), axis=1)]

# Optional: Normalize 'Rule to Enact' column for consistent matching
common_rule_texts = set(common_rules_df['Rule to Enact'].dropna().str.strip().str.lower())

# Compare with left-out rules (adjust column name if needed)
left_out_rules = left_out_df[left_out_df['Rule to Enact'].dropna().str.strip().str.lower().isin(common_rule_texts)]

# Combine both sets of matching rules
final_df = pd.concat([common_rules_df, left_out_rules], ignore_index=True)

# Save to a new CSV if needed
final_df.to_csv("All_Common_Rules.csv", index=False)

print(f"{len(common_rules_df)} common rules found across all states.")
print(f"{len(left_out_rules)} matching rules added from left-out tab.")
