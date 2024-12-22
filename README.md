
# Customer Feedback Data Cleaning Project

In this project, we use python to perform various tasks to clean a dataset of customer feedback. We do something a little different from other projects - in this specific project, we used the "faker" module from python libraries to helps us generate fake customer feedback data for us to clean and format. 

The main purpose of this project is to demonstrate the ability to use python to perform data cleaning tasks. 



## Link To Dataset

You can view the dataset by clicking the link below:

[View the dataset on Google Sheets](https://docs.google.com/spreadsheets/d/1rjjVOWhqHWr6vWTYD9XDPxOQQaAN8iJiDRq4kx9upNI/edit?usp=sharing)

This link will give you access to the full dataset.

## Dataset Before


Below is the messy dataset for reference:

| Customer_ID | Name                | Feedback                                   | Rating | Date_Submitted | Email                     |
|-------------|---------------------|-------------------------------------------|--------|----------------|---------------------------|
| 1           | Olivia Gutierrez    | Less according including subject keep small expect. | 1      | 2020-08-01     | victoria63@example.com    |
| 2           | Erik Webster        | N/A                                       | 5      |                | dcastillo@example.com     |
| 3           | Mathew Welch        | Man represent participant car along.      | 2      | 2023-12-28     |                           |
| 4           | Angela Blair        | Political let me window.                  | 1      | 12/03/2020     | michaelharding@example.org |
| 5           | Alicia Fernandez    |                                           | 3      |                | margaret59@example.com    |
| 6           |                     |                                           | -10    | 2022-03-18     | vdurham@example.com       |
| 7           | Bethany Hill        |                                           | 3      |                | invalid_email             |
| 8           | Connor Anderson     | N/A                                       | 1      | 24/12/2023     |                           |
| 9           | Amy Salinas         | Green difficult pull investment.          | 5      |                | tiffany23@example.com     |
| 10          | Brian Miller        |                                           | 2      |                | gregorydaniel@example.net |
| 11          | Leslie Mendoza      | Human program stuff among.                | 1      |                | moorelaura@example.net    |
| 12          | Jonathan Taylor     | N/A                                       | -10    | 2021-12-16     | lindarodriguez@example.net |
| 13          | James Weaver        | N/A                                       | 3      | 24/02/2021     | hjackson@example.com      |
| 14          | Diana Myers         |                                           | -10    |                |                           |
| 15          | Samuel West         | N/A                                       | 100    | 2020-03-22     | scottandre@example.com    |
| 16          | Christopher Smith   | N/A                                       | 2      |                | lopezjose@example.net     |
| 17          | John Morales        |                                           | -10    | 04/04/2024     | john58@example.org        |
| 18          | Tracy Robinson      | N/A                                       | 100    | 2021-06-19     | zgill@example.com         |
| 19          | Beth Castillo       | Me explain page a or especially unit base. | 3      | 21/01/2022     | adam77@example.com        |
| 20          | Marissa Pierce      | Bank eat process media reality.           | 4      |                | xschmidt@example.com      |

This table showcases the unprocessed version of the dataset.

## Dataset After

Below is the cleaned dataset for reference:

| Customer_ID | Name               | Feedback                                   | Rating | Date_Submitted | Email                     |
|-------------|--------------------|-------------------------------------------|--------|----------------|---------------------------|
| 1           | Angela Roberts     | No Feedback                               | 1      | 2022-12-19     | cmurphy@example.org       |
| 2           | Rachel Perry       | No Feedback                               | 1      | 2024-07-18     | karagarcia@example.com    |
| 3           | Unknown            | No Feedback                               | 1      | 2022-12-25     | abrock@example.com        |
| 4           | Nicole Lopez       | No Feedback                               | 5      |                | hancocksamantha@example.com |
| 6           | Meghan Valdez      | No Feedback                               | 5      |                | kent42@example.net        |
| 7           | Joseph Lopez       | No Feedback                               | 2      |                | vwhite@example.com        |
| 10          | Aaron Owen Dvm     | No Feedback                               | 2      | 2024-09-04     | pbaker@example.com        |
| 15          | Alyssa Gross       | No Feedback                               | 3      |                | zacharycox@example.com    |
| 17          | Jordan Perez       | No Feedback                               | 4      | 2021-09-19     | greencurtis@example.org   |
| 18          | Michael Peterson   | No Feedback                               | 2      |                | ymullen@example.net       |
| 19          | Dennis Douglas     | Low every before choice bar Congress.     | 1      |                | sarahcole@example.org     |
| 20          | Derek Carroll      | Both job operation single attention.      | 5      |                | saraleblanc@example.org   |

This table showcases the processed and cleaned version of the dataset.

## Python Sript:

```python
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



