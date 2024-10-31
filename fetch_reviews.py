import requests
import json
import pandas as pd

def load_api_key():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config.get("api_key")

def get_place_id(api_key, query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': api_key
    }
    response = requests.get(url, params=params)
    result = response.json()
    
    if 'results' in result and result['results']:
        return result['results'][0]['place_id']
    else:
        print("Place not found.")
        return None

def get_reviews(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'reviews',
        'key': api_key
    }
    response = requests.get(url, params=params)
    result = response.json()
    
    if 'result' in result and 'reviews' in result['result']:
        return result['result']['reviews']
    else:
        print("No reviews found.")
        return []

def save_reviews_to_csv(reviews, filename):
    if reviews:
        data = []
        for review in reviews:
            data.append({
                'Author': review.get('author_name'),
                'Rating': review.get('rating'),
                'Review': review.get('text'),
                'Time': review.get('relative_time_description')
            })
        df = pd.DataFrame(data)
        df.to_csv(f"data/{filename}", index=False)
        print(f"Reviews saved to data/{filename}")
    else:
        print("No reviews to save.")

if __name__ == "__main__":
    api_key = load_api_key()
    
    place_name = input("Enter the name of the place (default: 'Joe Fortes Seafood & Chop House'): ") or "Joe Fortes Seafood & Chop House"
    city = input("Enter the city (default: 'Vancouver'): ") or "Vancouver"
    output_file = input("Enter the name of the file to save the reviews (default: 'reviews.csv'): ") or "reviews.csv"
    
    query = f"{place_name} {city}"

    place_id = get_place_id(api_key, query)

    if place_id:
        reviews = get_reviews(api_key, place_id)
        
        if reviews:
            save_reviews_to_csv(reviews, output_file)
        else:
            print("No reviews available to save.")
    else:
        print("Unable to fetch reviews.")
