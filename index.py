 
"""
Create data.json file with all the mutual fund details
"""
import json
import os
import requests
import pandas as pd
from loguru import logger


session = requests.Session()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def mf_list():
    file = "mf.json"  # save inside data/
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.load(f)
            print("Data loaded from mf.json")
            return data
    else:
        url = 'https://api.mfapi.in/mf'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open(file, 'w') as f:
                json.dump(data, f, indent=4)
            print("Data saved to mf.json")
            return data
    return []

def get_mf_info(isin):
    if not isin:
        return None
    url = f'https://mf.captnemo.in/kuvera/{isin}'
    response = session.get(url)

    if response.status_code != 200:
        print(f"Error fetching NAV data for ISIN {isin}: {response.status_code}")
        return None
    data = response.json()
    if 'error' in data:
        print(f"Error in response for ISIN {isin}: {data['error']}")
        return None
    return data
def simplify_fund(fund):
    lump_min = fund.get("lump_min")
    sip_min = fund.get("sip_min")
    nav_data = fund.get("nav", {})
    latest_nav = nav_data.get("nav")
    min_investment = min(lump_min if lump_min is not None else float("inf"),sip_min if sip_min is not None else float("inf"))
    return {
        "Name": fund.get("name"),
        "Type": fund.get("fund_type"),
        "Category": fund.get("fund_category"),
        "Dividend": fund.get("reinvestment"),
        "aum": float(fund.get("aum", 0)),
        "expense_ratio": fund.get("expense_ratio"),
        "week_1": fund.get("returns", {}).get("week_1"),
        "year_1": fund.get("returns", {}).get("year_1"),
        "inception": fund.get("returns", {}).get("inception"),
        "Value": fund.get("volatility"),
        "min_amount":min_investment,
        "nav": latest_nav,
        "isin":fund.get("ISIN"),
        "ter":fund.get("expense_ratio"),
        "scheme_code":fund.get("scheme_code"),
        "fund_house":fund.get("fund_house")
    }
def append_to_json_array(output, file_path="src/routes/data1.json"):
    if not os.path.exists(file_path):
        # create a new JSON array with the first element
        with open(file_path, "w") as f:
            f.write("[\n")
            json.dump(output, f, indent=4)
            f.write("\n]")
    else:
        # Append to existing JSON array
        with open(file_path, "rb+") as f:
            f.seek(-1, os.SEEK_END)  # move back 1 char from end (the closing ])
            f.truncate()             # cut off the ]
        
        with open(file_path, "a") as f:
            f.write(",\n")
            json.dump(output, f, indent=4)
            f.write("\n]")

def save_fund_data(isin, nav_data):
    if not nav_data:
        return
    # Normalize nav_data
    if isinstance(nav_data, list):
        if not nav_data:
            return
        nav_data = nav_data[0]  # take first element of the list

    if not isinstance(nav_data, dict):
        logger.warning(f"Unexpected nav_data type for {isin}: {type(nav_data)}")
        return
    output = simplify_fund(nav_data)
    append_to_json_array(output)
def append_nav_history(scheme_code, file_path="./static/nav_history1.json", max_records=30):
    if not scheme_code:
        return
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = session.get(url)
    if response.status_code != 200:
        print(f"Error fetching NAV for scheme code {scheme_code}: {response.status_code}")
        return
    data = response.json()
    if "error" in data:
        print(f"Error in response for scheme code {scheme_code}: {data['error']}")
        return

    nav_history = data.get("data", [])[:max_records]
    nav_history_str = "|".join(f"{item['date']}:{item['nav']}" for item in nav_history)
    output = {
        "scheme_code": scheme_code,
        "scheme_name": data.get("meta", {}).get("scheme_name"),
        "nav_history": nav_history_str
    }

    # If file doesn't exist, create and start an array
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("[\n")
            json.dump(output, f, indent=4)
            f.write("\n]")
    else:
        # Append to existing JSON array
        with open(file_path, "r+") as f:
            f.seek(0, os.SEEK_END)  # Go to end of file
            f.seek(f.tell() - 2, os.SEEK_SET)  # Back up before closing bracket
            f.write(",\n")
            json.dump(output, f, indent=4)
            f.write("\n]")

    print(f"Appended NAV for scheme code {scheme_code} to {file_path}")
# append_nav_history("120166")
print()
if __name__ == "__main__":
    funds = mf_list()
    file_path = "static/nav_history1.json"
    file_path1 = "src/routes/data1.json"
    # Check if file exists before deleting
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")
    if os.path.exists(file_path1):
        os.remove(file_path1)
        print(f"{file_path1} has been deleted.")
    else:
        print(f"{file_path1} does not exist.")
    for index, fund in enumerate(funds):
        logger.info(f"Processing {index + 1}/{len(funds)}: {fund.get('schemeName')}")
        is_Visited= False
        for isin in [fund.get("isinGrowth"), fund.get("isinDivReinvestment")]:
            if not isin:
                continue
            nav_data = get_mf_info(isin)
            if nav_data is None:
                print(f"No data returned for ISIN {isin}, skipping...")
                continue # take first element of the list
            if isinstance(nav_data, list):
                if not nav_data:
                    print(f"Empty list returned for ISIN {isin}, skipping...")
                    continue
                nav_data = nav_data[0]
            if nav_data.get("reinvestment") != 'Z':
                continue
            is_Visited = True
            nav_data["scheme_code"] = fund.get("schemeCode")
            save_fund_data(isin, nav_data)
        if is_Visited:
            append_nav_history(fund.get("schemeCode"))
    old_file = "static/nav_history.json"
    new_file = "static/nav_history1.json"
    os.replace(new_file, old_file)  # This will overwrite old_file safely
    print(f"{old_file} replaced with {new_file}")
    old_file1 = "src/routes/data.json"
    new_file1 = "src/routes/data1.json"
    os.replace(new_file1,old_file1)
    print(f"{old_file1} replaced with {new_file1}")
    mf_file_path = "mf.json"
    if os.path.exists(mf_file_path):
        os.remove(mf_file_path)
        print(f"{mf_file_path} has been deleted.")
    else:
        print(f"{mf_file_path} does not exist.")

    
    
 