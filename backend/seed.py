import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 500
np.random.seed(42) # For reproducible results

# Data pools
claimant_types = ['Individual', 'Business', 'Municipality']
damage_categories = [
    'Property Damage', 'Relocation Expenses', 
    'Lost Agricultural Income', 'Business Interruption', 'Structural Damage'
]
statuses = ['Under Review', 'Approved', 'Disbursed', 'Rejected']
counsels = ['Smith & Associates', 'Gomez Legal', 'Patel Law Group', 'Rivera & Co', 'Chen Defenders']

# Helper to generate random dates
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

start_filing = datetime(2023, 1, 1)
end_filing = datetime(2026, 1, 1)

data = []

for i in range(1, NUM_ROWS + 1):
    claim_id = f"CLM-{10000 + i}"
    
    # Weighted choices for realism
    claimant = np.random.choice(claimant_types, p=[0.7, 0.25, 0.05])
    
    if claimant == 'Business':
        category = np.random.choice(['Business Interruption', 'Structural Damage', 'Property Damage'])
        requested = round(np.random.uniform(50000, 2500000), 2)
    elif claimant == 'Municipality':
        category = 'Structural Damage'
        requested = round(np.random.uniform(1000000, 10000000), 2)
    else:
        category = np.random.choice(['Property Damage', 'Relocation Expenses', 'Lost Agricultural Income'])
        requested = round(np.random.uniform(5000, 150000), 2)

    status = np.random.choice(statuses, p=[0.3, 0.2, 0.35, 0.15])
    
    # Logic for approved amounts
    if status in ['Approved', 'Disbursed']:
        # Usually approved for 60% to 100% of requested
        approved = round(requested * np.random.uniform(0.6, 1.0), 2) 
    elif status == 'Rejected':
        approved = 0.0
    else: # Under Review
        approved = None

    counsel = random.choice(counsels)
    filing_date = random_date(start_filing, end_filing)
    
    # Add resolution date if not under review
    if status != 'Under Review':
        resolution_date = random_date(filing_date, datetime.now()).strftime('%Y-%m-%d')
    else:
        resolution_date = None

    data.append({
        'Claim_ID': claim_id,
        'Claimant_Type': claimant,
        'Damage_Category': category,
        'Status': status,
        'Requested_Amount': requested,
        'Approved_Amount': approved,
        'Assigned_Counsel': counsel,
        'Filing_Date': filing_date.strftime('%Y-%m-%d'),
        'Resolution_Date': resolution_date
    })

# Create DataFrame and export
df = pd.DataFrame(data)
filename = "indemnification_claims_data.csv"
df.to_csv(filename, index=False)

print(f"Successfully generated {NUM_ROWS} rows of mock data into '{filename}'!")