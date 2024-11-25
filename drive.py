import random
import pandas as pd
import streamlit as st

# Step 1: Generate Driver Profiles
def generate_driver_profiles(num_drivers=10):
    profiles = []
    for _ in range(num_drivers):
        profile = {
            'driver_id': _,
            'age': random.randint(15, 70),
            'experience_years': random.randint(0, 50),
            'preferred_path': random.choice(['A', 'B']),
            'historical_choices': random.choices(['A', 'B'], k=30),
            'traffic_conditions': random.choice(['Clear', 'Moderate', 'Heavy']),
            'weather_conditions': random.choice(['Sunny', 'Rainy', 'Snowy']),
            'road_conditions': random.choice(['Normal', 'Construction', 'Accident']),
            'accident_history': random.choice([True, False])  # Randomly assign accident history
        }
        profiles.append(profile)

    new_driver = {
        'driver_id': num_drivers,
        'age': 18,
        'experience_years': 1,
        'preferred_path': 'B',
        'historical_choices': ['B'] * 20 + ['A'] * 10,
        'traffic_conditions': 'Clear',
        'weather_conditions': 'Sunny',
        'road_conditions': 'Normal',
        'accident_history': False
    }
    profiles.append(new_driver)

    return pd.DataFrame(profiles)

# Step 2: Analyze Choices
def analyze_choices(driver_profiles):
    reasons = {}
    for _, row in driver_profiles.iterrows():
        if row['preferred_path'] == 'A':
            if row['experience_years'] >= 5:
                reason = "Experienced driver with a good track record."
            elif row['historical_choices'].count('A') > 15:
                reason = "Habitual choice of path A."
            elif row['age'] > 30:
                reason = "Older driver, likely to prefer safer routes."
            elif row['traffic_conditions'] == 'Clear':
                reason = "Optimal conditions for path A."
            elif row['road_conditions'] == 'Construction':
                reason = "Chosen path A to avoid construction on path B."
            else:
                reason = "Other reasons not specified."

            reasons[row['driver_id']] = reason
            
        elif row['preferred_path'] == 'B':
            if row['age'] < 25:
                reason = "Young driver with limited experience."
            elif row['experience_years'] < 5:
                reason = "Driver has low experience."
            elif row['historical_choices'].count('B') > 15:
                reason = "Habitual choice of path B."
            elif row['traffic_conditions'] == 'Heavy':
                reason = "Chose path B to avoid heavy traffic on path A."
            elif row['road_conditions'] == 'Accident':
                reason = "Path B is risky due to an accident on the road."
            elif row['accident_history']:
                reason = "Driver has a history of accidents, making path B a risky choice."
            else:
                reason = "Other reasons not specified."
                
            reasons[row['driver_id']] = reason
            
    return reasons

# Step 3: Design Interventions
def design_interventions(driver_profiles):
    interventions = {}
    for _, row in driver_profiles.iterrows():
        if row['historical_choices'].count('B') > 15:
            suggested_path = 'A'
            incentive = random.uniform(0.5, 1.0)  # Higher incentive for habitual B choosers
        else:
            suggested_path = 'A'
            incentive = random.uniform(0.1, 0.5)

        intervention = {
            'driver_id': row['driver_id'],
            'incentive': incentive,
            'suggested_path': suggested_path
        }
        interventions[row['driver_id']] = intervention
    return interventions

# Main Streamlit Application
def main():
    st.title("Driver Profile Analysis Dashboard")

    # Sidebar for user input
    st.sidebar.header("User Input")
    num_drivers = st.sidebar.number_input("Number of Drivers", min_value=1, max_value=100, value=10)

    # Button to generate driver profiles
    if st.button('Generate Driver Profiles'):
        driver_profiles = generate_driver_profiles(num_drivers)
        st.subheader("Driver Profiles")
        st.dataframe(driver_profiles)

        # Analyze choices for drivers who prefer path A and B
        reasons_for_a_b = analyze_choices(driver_profiles)
        st.subheader("Reasons for Choosing Paths A and B")
        st.write(reasons_for_a_b)

        # Design interventions based on profiles
        interventions = design_interventions(driver_profiles)
        st.subheader("Interventions")
        st.write(interventions)

        # Visualization of choices
        st.subheader("Distribution of Preferred Paths")
        path_counts = driver_profiles['preferred_path'].value_counts()
        st.bar_chart(path_counts)

        # Save to CSV functionality
        if st.button('Save to CSV'):
            combined_data = []

            for driver_id, intervention in interventions.items():
                driver_data = driver_profiles.loc[driver_profiles['driver_id'] == driver_id].iloc[0]
                combined_data.append({
                    'driver_id': driver_id,
                    'age': driver_data['age'],
                    'experience_years': driver_data['experience_years'],
                    'preferred_path': driver_data['preferred_path'],
                    'incentive': intervention['incentive'],
                    'suggested_path': intervention['suggested_path'],
                    'reason_for_path_a_or_b': analyze_choices(driver_profiles).get(driver_id, "N/A")
                })

            combined_df = pd.DataFrame(combined_data)
            csv = combined_df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name='driver_profiles.csv', mime='text/csv')

if __name__ == "__main__":
    main()