import boto3
import pandas as pd
import re
import json
from datetime import datetime

endpoint_url = "https://mio.vkyc.cbi.prod.getkwikid.com"


s3 = boto3.client('s3', aws_access_key_id = "minio",
                  aws_secret_access_key="minio@123",
                  endpoint_url=endpoint_url, verify=False)

bucket_name = 'kwikid'

csv_file_path = 'accounts_data_13July_25Sep2023.csv'

df = pd.read_csv(csv_file_path)

lst = []
d = {}
# Assuming 'mobile_number' is the column name for the mobile numbers
mobile_numbers = df['mobile_number'].tolist()
account_creation_times = df['account_created_time'].tolist()
first_10_records = mobile_numbers
print(len(mobile_numbers))
count = 0

# print(sumati)
# Now, mobile_numbers contains all the mobile numbers from the CSV
for i in range(len(first_10_records)):
    input_date_str = account_creation_times[i]
    # print(type(input_date_str))
    target_date_str = "01-09-2023 00:00"

    # Define the date format
    date_format = "%d-%m-%Y %H:%M"

    # Parse the input and target dates
    input_date = datetime.strptime(input_date_str, date_format)
    target_date = datetime.strptime(target_date_str, date_format)
    # print(input_date)
    # print(target_date)
    # Compare the two dates
    if input_date > target_date:
        # print(f"{input_date_str} is greater than 1st September 2023.")

        d= {}
        count+=1
        d["mobile_number"] = first_10_records[i]
        d["account_created_time"] = account_creation_times[i]
        # mobile_number = "9079042188"
        print(count)
        print(first_10_records[i])
        # d['mobi'] = mobile_number
        print("Just outside fetching response")
        prefix = f"videokyc/logs/CBI/cbs/{first_10_records[i]}/"

        

    # List objects in the specified bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix = prefix)
        print("After fetching response:",response.keys())
        # Check if any objects were found
        print("Just outside contents loop")
        if 'Contents' in response:
            print("inside contents if")
            objects = response['Contents']
            print(len(objects))
            for obj in objects:
                count+=1
                
                object_key = obj['Key']
                # print(object_key)
                input_string = object_key

                # Define a regular expression pattern to match the desired text
                pattern = r'/([^/]+)_(\d{10})\.json'

                # Use re.search to find the pattern in the input string
                match = re.search(pattern, input_string)

                if match:
                    # Extract the text between the last '/' and '1689222169'
                    extracted_text = match.group(1)
                else:
                    # Handle the case when the pattern is not found
                    extracted_text = None

                # Print the result
                # print(extracted_text)
                #get api anme from key oath
                # d[extracted_text] = obj['total_time']
                
                try:
                    response = s3.get_object(Bucket=bucket_name, Key=object_key)

                    # Get the contents of the object
                    object_content = response['Body'].read()
                    # print("hello")
                    # print(object_content)
                    # You can now work with the object's content
                    # For example, print it
                    object = object_content.decode('utf-8') # Assuming it's a text-based file
                    obj = json.loads(object)
                    # print(obj['total_time'])
                    # d["total_time"] = obj['total_time']
                    # time = obj['total_time'].split('.')[1]
                    # d[extracted_text] = obj['total_time']
                    d.update({extracted_text:obj['total_time']})
                    
                except Exception as e:
                    # Handle exceptions if the object retrieval fails
                    print(e)
                #get_obejct from s3 using key path
                #read json file an dget total_time
                # d["total_time"] = obj['total_time']
                # with open("data.txt","a") as file:
                #     file.write(object_key +"\n")

                # object_size = obj['Size']
                # # Process the object metadata as needed
                # print(f"Object Key: {object_key}, Size: {object_size} bytes")
                # if count > 1:
                #     break
            
            lst.append(d)
        else:
            # print(f"No objects found in the specified bucket for {mobile_number}")
            pass

    # lst.append(d)
    print(lst)


    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(lst)

    # Specify the file name for the CSV
    csv_filename = 'output.csv'

    # Write the DataFrame to the CSV file
    df.to_csv(csv_filename, index=False)
# df = pd.DataFrame(lst)
# df.to_csv()

# import boto3
# import pandas as pd

# endpoint_url = 'https://vkycuat.centralbank.co.in:49164'

# s3 = boto3.client('s3', aws_access_key_id="minio",
#                   aws_secret_access_key="minio@123",
#                   endpoint_url=endpoint_url, verify=False)

# bucket_name = 'kwikid'

# csv_file_path = 'accounts_data_13July_25Sep2023.csv'

# df = pd.read_csv(csv_file_path)

# # Assuming 'mobile_number' is the column name for the mobile numbers
# mobile_numbers = df['mobile_number'].tolist()
# print(mobile_numbers)

# # Initialize an empty list to store all objects
# all_objects = []
# count = 0
# # Iterate through mobile numbers
# for mobile_number in mobile_numbers:
#     count+=1
#     print(count)
#     # Initialize the continuation token
#     continuation_token = None
    
#     # List objects in the specified bucket with a prefix
#     while True:
#         # Create a dictionary with the bucket name and prefix
#         list_params = {
#             'Bucket': bucket_name,
#             'Prefix': f"videokyc/logs/CBI/cbs/{mobile_number}/",
#         }
        
#         # Add continuation token to the parameters if it exists
#         if continuation_token:
#             list_params['ContinuationToken'] = continuation_token
        
#         # List objects
#         response = s3.list_objects_v2(**list_params)
        
#         # Check if any objects were found
#         if 'Contents' in response:
#             objects = response['Contents']

#             all_objects.extend(objects)
        
#         # Check if there are more results to retrieve
#         if 'NextContinuationToken' in response:
#             continuation_token = response['NextContinuationToken']
#         else:
#             break  # No more results
        
# # Now, all_objects contains all the objects from the S3 bucket
# for obj in all_objects:
#     object_key = obj['Key']
#     with open("data.txt","a") as file:
#         file.write(object_key +"\n")
#     object_size = obj['Size']
#     # Process the object metadata as needed
#     print(f"Object Key: {object_key}, Size: {object_size} bytes")




# Input string
# input_string = "videokyc/logs/CBI/cbs/9079042188/aadhaar_vault_1689222169.json"

# # Define a regular expression pattern to match the desired text
# pattern = r'/([^/]+)_1689222169'

# # Use re.search to find the pattern in the input string
# match = re.search(pattern, input_string)

# if match:
#     # Extract the text between the last '/' and '1689222169'
#     extracted_text = match.group(1)
# else:
#     # Handle the case when the pattern is not found
#     extracted_text = None

# # Print the result
# print(extracted_text)
