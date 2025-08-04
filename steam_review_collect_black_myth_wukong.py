import requests
import time
import pandas as pd
from datetime import datetime

# This script based on steam public method https://partner.steamgames.com/doc/store/getreviews



def fetch_review_data(app_id:int,output_csv_file:str,max_reviews_to_fetch:int,request_dalay_seconds:float):

    # --- Data Collection ---
    ALL_REVIEWS_DATA = []
    PREVIOUS_CURSORS = set()
    cursor = '*' # Start with the first page

    print(f"Starting to fetch Steam reviews for App ID: {app_id}...")

    while True:
        url = f"https://store.steampowered.com/appreviews/{app_id}"
        params = {
            'json': 1,
            #'language': 'english', # You can change this or remove for all languages
            'language': 'all',
            'cursor': cursor,
            'num_per_page': 100, # Max allowed is 100
            'filter': 'recent', # recent – sorted by creation time   ;  updated – sorted by last updated time  ;  'all' should not use with cursor
            # 'day_range': 365 # Uncomment to filter by reviews within the last 365 days
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()

            if data['success'] != 1:
                print(f"API Error: {data}. Stopping.")
                break

            reviews = data['reviews']
            if not reviews:
                print("No more reviews to fetch. Stopping.")
                break # No more reviews

            for review in reviews:
                # Extract and format the required data
                reviewer_name = review.get('author', {}).get('steamid', 'N/A') # Use Steam ID as a unique identifier for reviewer
                # Alternatively, if you want the displayed name (can be changed by user):
                # reviewer_name = review.get('author', {}).get('persona', 'N/A')
                
                reviewer_num_reviews = review.get('author', {}).get('num_reviews', 'N/A') 
                language = review.get('language','')
                steam_purchase = review.get('steam_purchase','')
                written_during_early_access = review.get('written_during_early_access','')
                
                review_date_unix = review.get('timestamp_created')
                review_date = datetime.fromtimestamp(review_date_unix).strftime('%Y-%m-%d %H:%M:%S') if review_date_unix else 'N/A'

                recommended = "Recommended" if review.get('voted_up') else "Not Recommended"

                hours_on_record = review.get('author', {}).get('playtime_forever', 0) / 60 # Convert minutes to hours
                hours_at_review_time = review.get('author', {}).get('playtime_at_review', 0) / 60 # Convert minutes to hours

                helpful_count = review.get('votes_up', 0)
                funny_count = review.get('votes_funny', 0)
                num_of_reply = review.get('comment_count', 0) # This is the number of comments on this review

                ALL_REVIEWS_DATA.append({
                    'review_id': review.get('recommendationid'),# Unique ID for the review
                    'weighted_vote_score': review.get('weighted_vote_score', 0.0), # How helpful the review is perceived
                    'language':language,
                    'review_text': review.get('review', '').replace('\n', ' ').replace('\r', ' '),
                    'date': review_date,
                    'recommand_or_not': recommended,
                    'reviewer_steamid': reviewer_name,
                    'reviewer_num_reviews': reviewer_num_reviews, # How many reviews this reviewer has cross all games
                    'steam_purchase': steam_purchase,
                    'hours_on_record': round(hours_on_record, 2), # Round to 2 decimal places
                    'hours_at_review_time': round(hours_at_review_time, 2),
                    'num_of_people_found_this_review_helpful': helpful_count,
                    'num_of_people_found_this_review_funny': funny_count,
                    'num_of_reply': num_of_reply,
                    'written_during_early_access': written_during_early_access,
                    # Clean newline characters
                })

            cursor = data.get('cursor') # Get cursor for the next page
            print(f"Fetched {len(reviews)} reviews. Total collected: {len(ALL_REVIEWS_DATA)}")

            if max_reviews_to_fetch and len(ALL_REVIEWS_DATA) >= max_reviews_to_fetch:
                print(f"Reached maximum reviews limit ({max_reviews_to_fetch}). Stopping.")
                break
            if cursor in PREVIOUS_CURSORS:
                print(f"Cursor loop detected (cursor: {cursor}). Stopping to avoid infinite loop.")
                break
            PREVIOUS_CURSORS.add(cursor)

            if not cursor or cursor =='*':
                print("No more cursor found. All reviews fetched. Stopping.")
                break

            # Be polite and avoid rate limiting
            time.sleep(request_dalay_seconds)

        except requests.exceptions.RequestException as e:
            print(f"Network or HTTP error: {e}. Retrying in {request_dalay_seconds*5} seconds...")
            time.sleep(request_dalay_seconds * 5) # Longer wait on error
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Stopping.")
            break

    # --- Save to CSV ---
    if ALL_REVIEWS_DATA:
        df = pd.DataFrame(ALL_REVIEWS_DATA)
        df.to_csv(output_csv_file, index=False, encoding='utf-8')
        print(f"\nSuccessfully saved {len(ALL_REVIEWS_DATA)} reviews to {output_csv_file}")
    else:
        print("\nNo reviews were fetched or an error occurred during fetching.")


if __name__ == '__main__':    
    # --- Configuration ---
    APP_ID = 2358720  # Black Myth: Wukong
    OUTPUT_CSV_FILE = "black_myth_wukong_steam_reviews_all.csv"
    MAX_REVIEWS_TO_FETCH = 1164000  # Set to an integer to limit for testing, or None for all
    REQUEST_DELAY_SECONDS = 0.1 # Be polite to the server

    fetch_review_data(APP_ID,OUTPUT_CSV_FILE,MAX_REVIEWS_TO_FETCH,REQUEST_DELAY_SECONDS)
