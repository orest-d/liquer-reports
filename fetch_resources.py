import yaml
import requests
from pathlib import Path

if __name__ == '__main__':
    path = Path("lqreports/resources")
    with open('resources.yaml') as f:
        resources = yaml.load(f, Loader=yaml.FullLoader)
        with open(path/"resources.yaml","w") as rf:
            yaml.dump(resources,rf)
        for key, entry in resources.items():
            print()
            print(key)
            print("-"*len(key))
            print(f"  url:     {entry['url']}")
            r=requests.get(entry['url'])
            print(f"  status:  {r.status_code}")
            with open(path/entry["filename"],"w") as rf:
                rf.write(r.text)
            
