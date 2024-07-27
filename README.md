# Player Clan Finder

## Overview

**Player Clan Finder** is a command-line tool designed to help users find which clan a specific Roblox player belongs to.
It retrieves data from the BigGames API to identify clans and their members, and checks if a given user is part of any clan.
Works up to the 1000th clan (can be changed in the code)

## Requirements

- Python 3.x
- `requests` library

## Installation
### Download latest release

Just download the built script in an .exe format and run it

### Clone and compile it yourself

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/player-clan-finder.git
    cd player-clan-finder
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment:**

    - **Windows:**

      ```bash
      .venv\Scripts\activate
      ```

    - **macOS/Linux:**

      ```bash
      source .venv/bin/activate
      ```

4. **Install the required libraries:**

    ```bash
    pip install requests
    ```

## Usage

1. **Run the program:**
  
    Double click on the exe file

  or
    
    ```bash
    python main.py
    ```

2. **Follow the prompts:**

    - Enter the Roblox User ID when asked.
    - Confirm if the displayed username is correct.
    - The program will search for the user in cached clan data.
    - View the progress of the search as clans are checked.

3. **Perform additional searches if desired:**

    After the search completes, you will be prompted to perform another search. Type `Y` to continue or `N` to exit the program.

## Configuration

- **API Endpoints:** The program uses the following API endpoints:
  - Clans: `https://biggamesapi.io/api/clans`
  - Clan Information: `https://biggamesapi.io/api/clan`
  - Roblox User Info: `https://users.roblox.com/v1/users`

- **Timeout and Retries:** The program uses a 10-second timeout for API requests and retries requests up to 5 times in case of failures.

## Troubleshooting

- **Connection Issues:** If you encounter connectivity issues, ensure you have an active internet connection and that the API endpoints are accessible.
- **API Rate Limits:** If the program slows down or stops, it might be due to API rate limits. Consider adding rate limiting or exponential backoff in the code.
- **Errors in Search:** Check the `app.log` file for detailed error messages if the program fails to fetch data or encounters issues.

## Contributing

Feel free to fork the repository, submit issues, or create pull requests with improvements or bug fixes.

## License

This project is licensed under the GNU General Public License (GPL) v3.0. See the [LICENSE](LICENSE) file for details.