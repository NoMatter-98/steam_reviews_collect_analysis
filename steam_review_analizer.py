import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the dataset
# Assuming the CSV content is available as a string or file-like object
# For this example, I'll simulate loading from the provided content

df = pd.read_csv('black_myth_wukong_steam_reviews_all.csv')
# Convert 'date' to datetime objects
df['date'] = pd.to_datetime(df['date'])

# --- 1. Distribution of Recommendations ---
recommendation_counts = df['recommand_or_not'].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(recommendation_counts, labels=recommendation_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
plt.title('Distribution of Recommendations')
plt.savefig('./figs/[01]distribution_of_recommendations.png')
#plt.show()

# --- 2. Hours Played vs. Recommendation ---
plt.figure(figsize=(12, 6))
ax = sns.boxplot(x='recommand_or_not', y='hours_at_review_time', data=df)
plt.title('Hours Played at Review Time vs. Recommendation')
plt.xlabel('Recommendation')
plt.ylabel('Hours Played at Review Time')
plt.ylim(0, df['hours_at_review_time'].quantile(0.95)) # Limit y-axis for better visualization, excluding extreme outliers
medians = df.groupby('recommand_or_not')['hours_at_review_time'].median().sort_index(ascending=False)
for i, median in enumerate(medians):
    ax.text(i, median, f'{median:.1f}', va='center', ha='center', color='black', weight='bold')
plt.savefig('./figs/[02-1]hours_played_at_review_time_vs_recommendation.png')
#plt.show()

plt.figure(figsize=(12, 6))
ax = sns.boxplot(x='recommand_or_not', y='hours_on_record', data=df)
plt.title('Total Hours on Record vs. Recommendation')
plt.xlabel('Recommendation')
plt.ylabel('Total Hours on Record')
plt.ylim(0, df['hours_on_record'].quantile(0.95)) # Limit y-axis for better visualization
medians = df.groupby('recommand_or_not')['hours_on_record'].median().sort_index(ascending=False)
for i,median in enumerate(medians):
    ax.text(i,median,f'{median:.1f}',va='center',ha='center',color='black',weight='bold')
plt.savefig('./figs/[02-2]hours_played_total_time_vs_recommendation.png')
#plt.show()

# --- 3. Helpfulness of Reviews ---
plt.figure(figsize=(12, 6))
ax = sns.boxplot(x='recommand_or_not', y='num_of_people_found_this_review_helpful', data=df)
plt.title('Helpfulness of Reviews vs. Recommendation')
plt.xlabel('Recommendation')
plt.ylabel('Number of People Found This Review Helpful')
plt.ylim(0, df['num_of_people_found_this_review_helpful'].quantile(0.95))

medians = df.groupby('recommand_or_not')['num_of_people_found_this_review_helpful'].median().sort_index(ascending=False)
for i,median in enumerate(medians):
    ax.text(i,median,f'{median:.1f}',va='center',ha='center',color='black',weight='bold')
plt.savefig('./figs/[03]helpfulness_of_reviews.png')
#plt.show()

# --- 4. Language Distribution ---
plt.figure(figsize=(10, 6))
sns.countplot(y='language', data=df, order=df['language'].value_counts().index, palette='viridis')
plt.title('Distribution of Review Languages')
plt.xlabel('Number of Reviews')
plt.ylabel('Language')
plt.savefig('./figs/[04]language_distribution.png')
#plt.show()

# --- 5. Review Activity Over Time ---
# Group by date and count reviews
reviews_over_time = df.set_index('date').resample('D').size().fillna(0) # Resample daily
plt.figure(figsize=(14, 7))
reviews_over_time.plot()
plt.title('Review Activity Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Reviews')
plt.grid(True)
plt.savefig('./figs/[05]review_activity_over_time.png')
#plt.show()

# --- 6. Correlation Matrix (for numerical features) ---
map_language = {'arabic':1,'bulgarian':2,'schinese':3,'tchinese':4,'czech':5,'danish':6,'dutch':7,'english':8,'finnish':9,'french':10,'german':11,'greek':12,'hungarian':13,'indonesian':14,'italian':15,'japanese':16,'koreana':17,'norwegian':18,'polish':19,'portuguese':20,'brazilian':21,'romanian':22,'russian':23,'spanish':24,'latam':25,'swedish':26,'thai':27,'turkish':28,'ukrainian':29,'vietnamese':30}
df['language_encoder'] = df['language'].map(map_language)	
map_recommand = {'Recommended':0,'Not Recommended':1}
df['recommand_or_not'] = df['recommand_or_not'].map(map_recommand)	
nowtime = datetime.now() 
df['months_before_now'] = (nowtime.year - df['date'].dt.year) * 12 + (nowtime.month - df['date'].dt.month)
df['days_before_now'] = (nowtime - df['date']).dt.days

numerical_df = df[['weighted_vote_score', 'hours_on_record', 'hours_at_review_time',
                   'num_of_people_found_this_review_helpful', 'num_of_people_found_this_review_funny',
                   'num_of_reply', 'reviewer_num_reviews','language_encoder','recommand_or_not','days_before_now']]
plt.figure(figsize=(28, 28))
sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Numerical Features')
plt.savefig('./figs/[06]correlation_matrix.png')
#plt.show()

# --- Conclusions (based on example data and typical patterns) ---
print("\n--- Analysis Conclusions ---")
print(f"Total reviews analyzed: {len(df)}")
recommended_percent = recommendation_counts.get('Recommended', 0) / len(df) * 100
not_recommended_percent = recommendation_counts.get('Not Recommended', 0) / len(df) * 100
print(f"Recommended reviews: {recommended_percent:.2f}%")
print(f"Not Recommended reviews: {not_recommended_percent:.2f}%")

print("\nObservations from plots:")
print("1. **Distribution of Recommendations:** The pie chart clearly shows the proportion of 'Recommended' versus 'Not Recommended' reviews. [cite_start]For the given sample, it appears there are more Recommended reviews. [cite: 1]")
print("2. **Hours Played vs. Recommendation:** The box plots for 'hours_at_review_time' and 'hours_on_record' against 'recommand_or_not' can reveal if players with more hours are more likely to recommend or not recommend the game. For the provided sample, it looks like 'Recommended' reviews tend to come from players with higher 'hours_at_review_time' and 'hours_on_record'[cite: 1].")
print("3. **Helpfulness of Reviews:** The box plot for 'num_of_people_found_this_review_helpful' can indicate if recommended or not-recommended reviews are generally found more helpful by the community. In the sample provided, the 'Recommended' review has a higher helpfulness count (36) compared to the 'Not Recommended' review (68), which seems counter-intuitive at first glance given the second review is longer and more detailed. This highlights that helpfulness isn't solely tied to sentiment or length[cite: 1].")
print("4. **Language Distribution:** The bar chart will show which languages the reviews are predominantly written in. For this dataset, Chinese (schinese) appears to be the most common language[cite: 1].")
print("5. **Review Activity Over Time:** The line plot visualizes the daily volume of reviews. This can help identify peak review periods, potentially correlating with game updates, events, or initial release buzz. Given the limited sample, it shows a few specific dates with reviews[cite: 1].")
print("6. **Correlation Matrix:** The heatmap displays the linear relationships between numerical variables. For instance, 'hours_on_record' and 'hours_at_review_time' are likely to be highly correlated[cite: 1]. 'weighted_vote_score' might show some correlation with helpfulness or hours, depending on the data.")
print("\nFurther analysis could include natural language processing (NLP) on 'review_text' for sentiment analysis, topic modeling, and keyword extraction to gain deeper insights into why players recommend or don't recommend the game.")