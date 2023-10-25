# import re

# # Input string
# input_string = "videokyc/logs/CBI/cbs/9079042188/aadhaar_vault_1689222169.json"

# # Define a regular expression pattern to match the desired text with any 10-digit number
# pattern = r'/([^/]+)_(\d{10})\.json'  # Matches any 10-digit number before '.json'

# # Use re.search to find the pattern in the input string
# match = re.search(pattern, input_string)

# if match:
#     # Extract the text between the last '/' and the 10-digit number
#     extracted_text = match.group(1)
#     ten_digit_number = match.group(2)
# else:
#     # Handle the case when the pattern is not found
#     extracted_text = None
#     ten_digit_number = None

# # Print the results
# print("Extracted Text:", extracted_text)
# print("10-Digit Number:", ten_digit_number)

# from datetime import datetime

# # Define the input date and the target date (1st September 2023)
# input_date_str = "13-07-2023 06:28"
# target_date_str = "01-09-2023 00:00"

# # Define the date format
# date_format = "%d-%m-%Y %H:%M"

# # Parse the input and target dates
# input_date = datetime.strptime(input_date_str, date_format)
# target_date = datetime.strptime(target_date_str, date_format)

# # Compare the two dates
# if input_date > target_date:
#     print(f"{input_date_str} is greater than 1st September 2023.")
# else:
#     print(f"{input_date_str} is not greater than 1st September 2023.")



import re
import csv

# Define your log line
log_line = '10.16.34.198 - - [03/Jun/2023:13:25:07 +0530] "POST /v1/user/init HTTP/1.0" 405 559 "https://vkyccug.centralbank.co.in:5560/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"'

# Define a regular expression pattern to extract relevant information
log_pattern = r'([\d.]+) - - \[([\w:/]+\s[+\-]\d{4})\] "(\w+) ([^"]+\/v1/user/init[^"]*) HTTP/\d\.\d" (\d+) (\d+) "([^"]+)" "([^"]+)"'

# Match the log line against the pattern
match = re.search(log_pattern, log_line)

if match:
    # Extract the matched groups
    ip_address = match.group(1)
    timestamp = match.group(2)
    method = match.group(3)
    api = match.group(4)
    status_code = match.group(5)
    response_size = match.group(6)
    referrer = match.group(7)
    user_agent = match.group(8)

    # Create a CSV file and write the extracted fields
    with open('new.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['IP', 'Timestamp', 'Method', 'API', 'Status Code', 'Response Size', 'Referrer', 'User-Agent'])
        csv_writer.writerow([ip_address, timestamp, method, api, status_code, response_size, referrer, user_agent])
