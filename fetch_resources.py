import yaml
import requests
from pathlib import Path

if __name__ == '__main__':
    with open('resources.yaml') as f:
        resources = yaml.load(f, Loader=yaml.FullLoader)
        for key, entry in resources.items():
            print()
            print(key)
            print("-"*len(key))
            print(f"  url:     {entry['url']}")
            r=requests.get(entry['url'])
            print(f"  status:  {r.status_code}")
            with open(Path("lqreports/resources")/entry["filename"],"w") as rf:
                rf.write(r.text)
            
