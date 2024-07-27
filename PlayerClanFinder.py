import requests
import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://biggamesapi.io/api"
CLANS_URL = f"{BASE_URL}/clans"
CLAN_INFO_URL = f"{BASE_URL}/clan"
ROBLOX_FETCH_USER_URL = "https://users.roblox.com/v1/users"

def is_response_ok(status_code, request_type):
    if status_code == 200:
        return True
    else:
        print(f"Error: {status_code}, for {request_type}")
        return False

def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_clans(session, page_number, page_size):
    try:
        response = session.get(CLANS_URL, params={
            'page': page_number,
            'pageSize': page_size,
            'sort': 'Points',
            'sortOrder': 'desc'
        }, timeout=10)
        if is_response_ok(response.status_code, "fetch clans"):
            return response.json().get('data', [])
    except requests.RequestException as e:
        logging.error(f"Failed to fetch clans: {e}")
    return []

def fetch_clan_info(session, clan_name):
    try:
        response = session.get(f"{CLAN_INFO_URL}/{clan_name.upper()}", timeout=10)
        if is_response_ok(response.status_code, "fetch clan info"):
            return response.json().get('data', {})
    except requests.RequestException as e:
        logging.error(f"Failed to fetch clan info for {clan_name}: {e}")
    return {}

def find_user(user_id, all_clans):
    page_size = 20
    total_clans = len(all_clans)
    found_clan = None

    def check_clan(clan):
        nonlocal found_clan
        if found_clan:
            return None
        
        clan_name = clan.get('Name')
        if clan_name:
            members = fetch_clan_info(session, clan_name).get('Members', [])
            for member in members:
                if int(member.get('UserID')) == int(user_id):
                    found_clan = clan_name.upper()
                    return found_clan
        return None
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_clan, clan) for clan in all_clans]
        for current_clan_counter, future in enumerate(futures, start=1):
            result = future.result()
            if found_clan:
                sys.stdout.write(f"\rChecking {all_clans[current_clan_counter-1].get('Name')} ... {current_clan_counter} out of {total_clans}")
                sys.stdout.flush()
                break
            sys.stdout.write(f"\rChecking {all_clans[current_clan_counter-1].get('Name')} ... {current_clan_counter} out of {total_clans}")
            sys.stdout.flush()

    return found_clan

def fetch_roblox_user(user_id):
    try:
        response = requests.get(f"{ROBLOX_FETCH_USER_URL}/{user_id}", timeout=10)
        if is_response_ok(response.status_code, "roblox user fetch"):
            return response.json().get('name')
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Roblox user: {e}")
    return False

def main():
    global session
    session = create_session()
    all_clans = []  # Cache for clans data
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        verified_user = False
        while not verified_user:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Input the User ID")
            user_id = input().strip()
            
            username = fetch_roblox_user(user_id)
            if username:
                print(f"Are you looking for {username}? (Y/N)")
                user_input = input().strip().upper()
                if user_input == "Y":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Searching...")
                    verified_user = True
            else:
                print("User not found")
                os.system("pause")
        
        # Fetch clans if not already cached or if needed to refresh
        if not all_clans:
            amount_of_pages = 5
            page_size = 200

            # Fetch all clans
            for page in range(1, amount_of_pages + 1):
                clans = fetch_clans(session, page, page_size)
                if not clans:
                    break
                all_clans.extend(clans)

        result = find_user(user_id, all_clans)
        os.system('cls' if os.name == 'nt' else 'clear')
        if result:
            print(f"User found in clan {result}")
        else:
            print("User not found in any clan")
        os.system("pause")

        # Ask user if they want to perform another search
        print("Do you want to perform another search? (Y/N)")
        user_input = input().strip().upper()
        if user_input != "Y":
            break

if __name__ == "__main__":
    main()
