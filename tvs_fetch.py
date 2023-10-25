import requests

# Replace 'your-url-here' with the actual pre-signed URL you generated
url = ' https://rcu-imagestore.s3.amazonaws.com/flamingo.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA3R25BEB7GE7KEB5P%2F20231025%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20231025T074252Z&X-Amz-Expires=350000&X-Amz-SignedHeaders=host&X-Amz-Signature=60571ed151ee1f120ebe684add147e3532554a8868f9f3b73046c7a87f6e88f7'

# Send an HTTP GET request to the pre-signed URL
response = requests.get(url)

if response.status_code == 200:
    # The request was successful, and the object content is stored in response.content
    with open('downloaded_file.jpeg', 'wb') as f:
        f.write(response.content)
    print("Object downloaded successfully.")
else:
    print("Failed to download the object. Status code:", response.status_code)
