# PyScholar
This is a tiny project that sends sms notifications based on the specific scholar profile changes about:
* Publications Count
* H-index Changes
* Citations Changes

PyScholar will checks the specific scholar page repeatitively and sends sms notification if there was any changes in the above titles.


## Usage
1. cp .env-example .env and fill values
2. cp result-example.json result.json
3. Run the compose file
   ```
   docker compose up -d
   ```
