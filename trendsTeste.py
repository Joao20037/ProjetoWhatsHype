from serpapi import GoogleSearch
import pandas as pd

params = {
  "engine": "google_trends",
  "q": "madonnna",
  "data_type": "TIMESERIES",
  "api_key": "4d73f4242018e9905d140bd94243ec92fc7c84b6ace1965607357bff0748a011"
}

search = GoogleSearch(params)
results = search.get_dict()
interest_over_time = results

df = pd.DataFrame(results["interest_over_time"]["timeline_data"])
print(df)
# print(json.dumps(results, indent=4))