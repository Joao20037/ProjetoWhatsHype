from serpapi import GoogleSearch
import csv

def parse_results(results):
    parsed_results = []
    for result in results:
        parsed_result = {
            'title': result['title'],
            'link': result['link'],
            'channel_name': result['channel']['name'],
            'channel_link': result['channel']['link'],
            'views': result.get('views', ''),
            'description': result.get('description', ''),
            'length': result.get('length', ''),
            'thumbnail': result['thumbnail']['static']
        }
        parsed_results.append(parsed_result)
    return parsed_results

def save_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = results[0].keys() if results else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

params = {
    'engine': "youtube",
    'search_query': "Música",
    'api_key': "4d73f4242018e9905d140bd94243ec92fc7c84b6ace1965607357bff0748a011"
}

search = GoogleSearch(params)
json_response = search.get_json()
video_results = json_response.get('video_results', [])

if video_results:
    parsed_results = parse_results(video_results)
    save_to_csv(parsed_results, 'youtube_results.csv')
    print("Results saved to youtube_results.csv")
else:
    print("No video results found.")
