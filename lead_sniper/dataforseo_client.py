import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DataForSEOClient:
    def __init__(self):
        self.login = os.getenv("DATAFORSEO_LOGIN")
        self.password = os.getenv("DATAFORSEO_PASSWORD")
        self.base_url = "https://api.dataforseo.com/v3/"

    def post(self, path, data):
        url = self.base_url + path
        response = requests.post(url, auth=HTTPBasicAuth(self.login, self.password), json=data)
        return response.json()

    def search_leads(self, query: str):
        """Lance une recherche SERP pour trouver des leads récents."""
        post_data = [{
            "language_code": "fr",
            "location_code": 2250, # France
            "keyword": query,
            "device": "desktop",
            "os": "windows",
            "depth": 100 
        }]
        
        response = self.post("serp/google/organic/live/advanced", post_data)
        
        results = []
        if response.get("tasks"):
            for task in response["tasks"]:
                if task.get("result"):
                    for result in task["result"]:
                        if result.get("items"):
                            for item in result["items"]:
                                if item.get("type") == "organic":
                                    results.append({
                                        "title": item.get("title"),
                                        "snippet": item.get("description"),
                                        "url": item.get("url")
                                    })
        return results
