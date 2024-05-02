from serpapi import GoogleSearch

params = {
  "engine": "google_trends",
  "q": "coffee,milk,bread,pasta,steak",
  "data_type": "TIMESERIES",
  "api_key": "4d73f4242018e9905d140bd94243ec92fc7c84b6ace1965607357bff0748a011"
}

search = GoogleSearch(params)
results = search.get_dict()
interest_over_time = results["interest_over_time"]


print(results)
