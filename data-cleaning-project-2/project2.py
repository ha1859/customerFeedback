import pandas as pd
import numpy as np
import random
from faker import Faker
import re

# Initialize Faker library for fake data generation. This is creating an object
fake = Faker()

# Step 1: Generate Messy Data
data = {
    "Customer_ID": [i for i in range(1, 21)],
    "Name": [fake.name() if random.random() > 0.1 else None for _ in range(20)],  # Random missing values
    "Feedback": [
        random.choice([
            fake.sentence(), "N/A", "", None  # Mix of real feedback, N/A, blanks, and nulls
        ]) for _ in range(20)
    ],
    "Rating": [random.choice([1, 2, 3, 4, 5, 100, -10]) for _ in range(20)],  # Outliers included
    "Date_Submitted": [
        random.choice([
            fake.date_this_decade().strftime("%Y-%m-%d"),
            fake.date_this_decade().strftime("%d/%m/%Y"),  # Mixed formats
            None
        ]) for _ in range(20)
    ],
    "Email": [
        fake.email() if random.random() > 0.1 else random.choice(["invalid_email", None]) for _ in range(20)
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Step 2: Save Dataset to CSV (if needed for re-use)
df.to_csv("messy_customer_feedback.csv", index=False)

print("Generated Messy Dataset:\n")
print(df)

# === Cleaning Tasks Start Here ===

# 1. Handle Missing Values
print("\n1. Handling Missing Values...")
print("Before:\n", df.isnull().sum())
# Fill 'Name' and 'Feedback' missing values with placeholders
df['Name'] = df['Name'].fillna("Unknown")
df['Feedback'] = df['Feedback'].replace(["N/A", "", None], "No Feedback")
# Drop rows with missing 'Email' since it's critical
df = df.dropna(subset=['Email'])
print("After:\n", df.isnull().sum())



# 2. Standardize Customer Names
print("\n2. Standardizing Customer Names...")
df['Name'] = df['Name'].str.title()



# 3. Format Dates Consistently
print("\n3. Formatting Dates...")
print("Before:\n", df['Date_Submitted'].head())
df['Date_Submitted'] = pd.to_datetime(df['Date_Submitted'], errors='coerce')
print("After:\n", df['Date_Submitted'].head())




# 4. Handle Outliers in Ratings
print("\n4. Handling Outliers in Ratings...")
print("Before:\n", df['Rating'].describe())
Q1 = df['Rating'].quantile(0.25)
Q3 = df['Rating'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
# Filter out outliers
df = df[(df['Rating'] >= lower_bound) & (df['Rating'] <= upper_bound)]
print("After:\n", df['Rating'].describe())




# 5. Validate Email Addresses
print("\n5. Validating Email Addresses...")
def is_valid_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.[a-z]{2,}$", email))

# Apply email validation
df['Valid_Email'] = df['Email'].apply(lambda x: is_valid_email(x))
# Keep only valid emails
df = df[df['Valid_Email']]
df = df.drop(columns=['Valid_Email'])
print("After Validation:\n", df['Email'].head())

# Final Cleaned Dataset
print("\nFinal Cleaned Dataset:\n")
print(df)

# Optional: Save the cleaned data to a new CSV file
df.to_csv("cleaned_customer_feedback.csv", index=False)
print("\nCleaned data saved to 'cleaned_customer_feedback.csv'")

