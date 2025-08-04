import pandas as pd

# load csv
with open("black_myth_wukong_steam_reviews_all.csv",mode='r',encoding='utf-8') as file:
    csv_data = file.read()

# Read the data into a DataFrame
#df = pd.read_csv(StringIO(csv_data))
df = pd.read_csv("black_myth_wukong_steam_reviews_all.csv")

# Filter for English and Chinese reviews with review_text length >= 80 characters
df['characters'] = df['review_text'].str.len()
df_filtered = df[(df['language'].isin(['english', 'schinese'])) & (df['characters'] >= 80)].copy()

# Convert 'date' to datetime and extract month
df_filtered['date'] = pd.to_datetime(df_filtered['date'])
df_filtered['month'] = df_filtered['date'].dt.month

# Sort by month and then by weighted_vote_score
df_sorted = df_filtered.sort_values(by=['month', 'weighted_vote_score'], ascending=[True, False])

# Calculate proportions for each month
month_proportions = df_sorted['month'].value_counts(normalize=True)

# Determine the number of samples for each month based on overall proportion
total_samples = 300
samples_per_month = (month_proportions * total_samples).round().astype(int)

# Adjust if total samples are not exactly 300 due to rounding
samples_diff = total_samples - samples_per_month.sum()
if samples_diff != 0:
    # Distribute the difference to the months with the largest remainders
    remainders = (month_proportions * total_samples) - samples_per_month
    if samples_diff > 0:
        top_months = remainders.nlargest(samples_diff).index
        samples_per_month.loc[top_months] += 1
    else:
        bottom_months = remainders.nsmallest(abs(samples_diff)).index
        samples_per_month.loc[bottom_months] -= 1

# Perform stratified sampling with language distribution
sampled_df_list = []
for month, num_samples in samples_per_month.items():
    monthly_df = df_sorted[df_sorted['month'] == month]
    if not monthly_df.empty and num_samples > 0:
        # Calculate language distribution (80% English, 20% Chinese)
        english_samples = int(num_samples * 0.8)
        chinese_samples = num_samples - english_samples
        
        # Sample English reviews
        english_df = monthly_df[monthly_df['language'] == 'english']
        if not english_df.empty:
            english_samples = min(english_samples, len(english_df))
            sampled_df_list.append(english_df.head(english_samples))
        
        # Sample Chinese reviews
        chinese_df = monthly_df[monthly_df['language'] == 'schinese']
        if not chinese_df.empty:
            chinese_samples = min(chinese_samples, len(chinese_df))
            sampled_df_list.append(chinese_df.head(chinese_samples))
            
sampled_df = pd.concat(sampled_df_list).reset_index(drop=True)

# Drop the temporary 'month' column before saving
sampled_df = sampled_df.drop(columns=['month'])

# Save the sampled data to a new CSV file
output_file = 'black_myth_wukong_steam_reviews_300_new.csv'
sampled_df[['weighted_vote_score','language','review_text','characters','date','recommand_or_not']].to_csv(output_file, index=False)

print(f"Sampled data saved to {output_file}")
print("\nFirst 5 rows of the sampled data:")
print(sampled_df.head())
print("\nInformation about the sampled data:")
print(sampled_df.info())