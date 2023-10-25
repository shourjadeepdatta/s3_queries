from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import requests
import datetime
import PyPDF2
import boto3
import pandas as pd
import os
import re
import fillpdf
from fillpdf import fillpdfs
import json
from datetime import datetime
# import fitz
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.pdfgen import canvas
import shutil
import pdfkit
from xhtml2pdf import pisa
import sys
from weasyprint import HTML


endpoint_url = "https://mio.vkyc.cbi.prod.getkwikid.com"
os.environ['WEXPY_USE_GTK'] = '3'

s3 = boto3.client('s3', aws_access_key_id = "minio",
                  aws_secret_access_key="minio@123",
                  endpoint_url=endpoint_url, verify=False)

bucket_name = 'kwikid'
lst = []
all_data = []
data_lst = []
folder_name = 'merged_new'
file_path = 'daily_2023-09-20.xlsx'
pdf_files = ['a4_1.pdf', 'a4_2.pdf', 'a4_3.pdf']
columns_to_read = ['mobile_number','session_id']
df = pd.read_excel(file_path,sheet_name='Account Data' ,usecols=columns_to_read)
print(len(df['mobile_number']))
l = len(df['mobile_number'])
os.makedirs(folder_name, exist_ok=True)
dpi = 500
audit_ids = []


icon_mapper = {
    "False":"red-x-icon.svg",
    "True":"tick-green-icon.svg"
}

for i in range(20):

    url = f"https://vkyc.centralbank.co.in/api/v1/getAllUserSession/CBI/{df['session_id'][i]}"

    payload = "{\"type\":\"session_id\"}"
    headers = {
    'Content-Type': 'application/json;charset=utf-8',
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'cross-site',
    'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Mode': 'cors',
    'Host': 'vkyc.centralbank.co.in',
    'Origin': 'https://auat.vkyc.getkwikid.com:9090',
    'Content-Length': '21',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Referer': 'https://auat.vkyc.getkwikid.com:9090/',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJDQkkiLCJpc3MiOiJpcHZfYXBpX0lvbmljQXBwIiwiYWRtaW5faWQiOiJDQklfYWRtaW4iLCJleHAiOjE2OTkxNjMxMzgsImlhdCI6MTY5NjU3MTEzOCwiYXVkIjoidXNyIn0.d1kb9vUCw_Z7qHTPfOo1w9WbakgDTGjv_O87GBPvDug'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    data = response.json()
    audit_ids.append(data['session_list'][0]['audit_id'])
    print(type(data))


for i in range(20):
    
    prefix = f'videokyc/summary/CBI/{df["mobile_number"][i]}/{df["session_id"][i]}/'
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix = prefix)


    if 'Contents' in response:
        # print("inside contents if")
        objects = response['Contents']
        # print(len(objects))

        for obj in objects:
            object_key = obj['Key']
            second_pdf = f"videokyc/summary/CBI/{df['mobile_number'][i]}/{df['session_id'][i]}/aadhaar_redacted.pdf"
            lst.append(object_key)
            print(object_key)
            print("Just outside main if")
            # object_content = response['Body'].read()
            if object_key == f"videokyc/summary/CBI/{df['mobile_number'][i]}/{df['session_id'][i]}/{df['session_id'][i]}.pdf":

                try:
                    response = s3.get_object(Bucket=bucket_name, Key=object_key)

                    # Get the contents of the object
                    # object_content = response['Body'].read()
                    with open("pdf1.pdf",'wb') as file1:
                        file1.write(response['Body'].read())
                    
                except Exception as e:
                    # Handle exceptions if the object retrieval fails
                    print(e)
                
                

                url = f"https://vkyc.centralbank.co.in/api/v1/admin/get_audit_report/{audit_ids[i]}"

                payload = {}
                headers = {
                'auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJDQkkiLCJpc3MiOiJpcHZfYXBpX0lvbmljQXBwIiwiYWRtaW5faWQiOiJDQklfYWRtaW4iLCJleHAiOjE2OTkwOTQzMTQsImlhdCI6MTY5NjUwMjMxNCwiYXVkIjoidXNyIn0.ompLedszTLyUVAqUpxMF--6QEMGMFGh_yQtWxpKf2uc'
                }

                response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                audit_data = response.json()
                # print(response.json())

                # # Create a PDF document
                # print(data)
                data_lst.append(audit_data)
                if audit_data:

                    pdf_filename = "example.pdf"
                    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
                    user_id = df['mobile_number'][i]
                    auditor = data.get('auditor', '')
                    # checklist_data = data.get('checklist_data', '')
                    audit_time = float(data.get('audit_init_time',0)) - float(data.get('audit_end_time',0))
                    epoch_timestamp = 1665019709

                    # Convert to a datetime object
                    dt_object = datetime.fromtimestamp(epoch_timestamp)

                    # Format the datetime object as "05 Oct 2023 4:08:29 PM"
                    epoch_timestamp = dt_object.strftime("%d %b %Y %I:%M:%S %p")

                    # print(formatted_date_time)
                    if audit_data['audit_result'] == '1':
                        msg = "Approved"
                        audit_result = "tick-green-icon.svg"
                    else:
                        msg = audit_data['feedback']
                        audit_result = "red-x-icon.svg"

                    # all_data.append(data)
                    print("inside green tick")
                    html = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        
                        <style>
                        @page {
                            size: 600mm 350mm; /* Landscape, with custom width and height */
                            margin: 1cm; /* Adjust margins as needed */
                        }
                        
                        body {
                            margin: 100px;
                        }
                            table {
                            width: 100%;
                            border-collapse: collapse;
                        }

                        th, td {
                            border: 1px solid black;
                            padding: 8px;
                            text-align: center;
                            width: 700px;
                        }
                        .tbl{
                            font-family: "Roboto", "Helvetica", "Arial", sans-serif;
                        }
                        

                        th {
                            background-color: lavender;
                        }

                        /* Remove the border for the right side of cells (vertical lines) */
                        td {
                            border-right: none;
                        }

                        tr:nth-child(even) {
                            background-color: white;
                        }

                        tr:nth-child(odd) {
                            background-color: lightgray;
                        }
                        </style>
                    </head>
                    <body>

                    <table class="tbl">
                        <tr>
                            <th>AUDIT RESULT</th>
                            <th>USER ID</th>
                            <th>AUDITOR</th>
                            <th>AUDIT TIME</th>
                            <th>Checklist Data</h>
                            <th>FEEDBACK</th>
                            
                        </tr>
                    """

                    
                    html += f"""
                        <tr>
                            <td><img src="{audit_result}" alt="Icon" width="20" height="20"></td>
                            <td>{df['mobile_number'][i]}</td>
                            <td>{audit_data.get('auditor',"")}</td>
                            <td>{epoch_timestamp}</td>

                            <td>Customer livliness check <img src="{icon_mapper[str(audit_data.get("checklist_data")['Customer livliness check'])]}" alt="Icon" width="20" height="20"><br>Facematch with AadhaarXML <img src="{icon_mapper[str(audit_data.get("checklist_data")['Facematch with AadhaarXML'])]}" alt="Icon" width="20" height="20"><br>Facematch with Pan<img src="{icon_mapper[str(audit_data.get("checklist_data")['Facematch with Pan'])]}" alt="Icon" width="20" height="20"><br>Locate Branch<img src="{icon_mapper[str(audit_data.get("checklist_data")['Locate Branch'])]}" alt="Icon" width="20" height="20"><br>Location in India<img src="{icon_mapper[str(audit_data.get("checklist_data")['Location in India'])]}" alt="Icon" width="20" height="20"><br>Pan Card<img src="{icon_mapper[str(audit_data.get("checklist_data")['Pan Card'])]}" alt="Icon" width="20" height="20"><br>Questions<br>Selfie<img src="{icon_mapper[str(audit_data.get("checklist_data")['Selfie'])]}" alt="Icon" width="20" height="20"><br>Signature Match<img src="{icon_mapper[str(audit_data.get("checklist_data")['Signature Match'])]}" alt="Icon" width="20" height="20"></td>
                            
                            <td>{msg}</td>
                            

                            
                        </tr>
                        """

                    html += """
                    </table>

                    </body>
                    </html>
                    """
                                                
                        # Save the generated HTML to a file or use it as needed
                        # with open("output.html", "w") as html_file:
                        #     html_file.write(html)

                        # pdfkit.from_file('output.html', 'a4_2.pdf')
                    
                        # Save the generated HTML to a file or use it as needed
                    # with open(f"{folder_name}/{df['mobile_number'][i]}.html", "w") as html_file:
                    #     html_file.write(html)
                with open("my_html_file.html", "w") as file:
                    file.write(html)

                # Convert the local HTML file to PDF
                # pdfkit.from_file("my_html_file.html", "a4_2.pdf")
                # HTML(string=html).write_pdf("a4_2.pdf")
                page_width = 2560  # 2560 pixels
                page_height = 1600  # 1600 pixels

                # Generate the PDF with the specified page size
                pdf_options = {
                    'page-size': f'{page_width}x{page_height}',
                    'margin-top': '0mm',  # Set margins to zero for consistency
                    'margin-right': '0mm',
                    'margin-bottom': '0mm',
                    'margin-left': '0mm',
                }
                with open("pdf2.pdf", "wb") as file2:
                    pisa.CreatePDF(html, dest=file2, pdf_options=pdf_options)
                
                fillpdfs.get_coordinate_map('Admin _ Central bank of India.pdf', 'template.pdf')
                

                try:
                    response = s3.get_object(Bucket=bucket_name, Key=second_pdf)

                    # Get the contents of the object
                    # object_content = response['Body'].read()
                    with open("pdf3.pdf",'wb') as file3:
                        file3.write(response['Body'].read())

                    
                    # object = object_content.decode('utf-8') # Assuming it's a text-based file
                    # obj = json.loads(object)
                    
                except Exception as e:
                    # Handle exceptions if the object retrieval fails
                    print(e)
                
                with open('pdf1.pdf', 'rb') as file1, open('pdf2.pdf', 'rb') as file2, open('pdf3.pdf', 'rb') as file3:
                    # page_width = 200.276  # Letter size width in points
                    # page_height = 300.890
                    # Create PDF reader objects for each file

                    try:
                        pdf_reader1 = PyPDF2.PdfReader(file1)
                        pdf_reader2 = PyPDF2.PdfReader(file2)
                        pdf_reader3 = PyPDF2.PdfReader(file3)
                    

                        # Create a PDF writer object to write the merged PDF
                        pdf_writer = PyPDF2.PdfWriter()

                        # Add pages from the first PDF
                        for page_num in range(len(pdf_reader1.pages)):
                            page = pdf_reader1.pages[page_num]
                            pdf_writer.add_page(page)

                        # Add pages from the second PDF
                        for page_num in range(len(pdf_reader2.pages)):
                            page = pdf_reader2.pages[page_num]
                            # page.mediabox.lower_left = (0, 0)
                            # page.mediabox.upper_right = (page_width, page_height)
                            pdf_writer.add_page(page)

                        # Add pages from the third PDF
                        for page_num in range(len(pdf_reader3.pages)):
                            page = pdf_reader3.pages[page_num]
                            pdf_writer.add_page(page)

                        # Save the merged PDF to the output file
                        output_file_path = f'{folder_name}/{df["mobile_number"][i]}.pdf'  # Replace with your desired output file name
                        with open(output_file_path, 'wb') as output:
                            pdf_writer.write(output)
                    except Exception as e:
                        print(e)

print(data_lst)


#                     if audit_data.get("checklist_data"):
#                         # all_data.append(data)
#                         print("inside green tick")
#                         html = """
#                         <!DOCTYPE html>
#                         <html>
#                         <head>
                         
#                             <style>
#                             @page {
#                                 size: 600mm 350mm; /* Landscape, with custom width and height */
#                                 margin: 1cm; /* Adjust margins as needed */
#                             }
                            
#                             body {
#                                 margin: 100px;
#                             }
#                                 table {
#                                 width: 100%;
#                                 border-collapse: collapse;
#                             }

#                             th, td {
#                                 border: 1px solid transparent;
#                                 padding: 8px;
#                                 text-align: center;
#                                 width: 800px;
#                             }
#                             .tbl{
#                                 font-family: "Roboto", "Helvetica", "Arial", sans-serif;
#                             }
                            

#                             th {
#                                 background-color: lavender;
#                             }

#                             /* Remove the border for the right side of cells (vertical lines) */
#                             td {
#                                 border-right: none;
#                             }

#                             tr:nth-child(even) {
#                                 background-color: white;
#                             }

#                             tr:nth-child(odd) {
#                                 background-color: lightgray;
#                             }
#                             </style>
#                         </head>
#                         <body>

#                         <table class="tbl">
#                             <tr>
#                                 <th>AUDIT RESULT</th>
#                                 <th>USER ID</th>
#                                 <th>AUDITOR</th>
#                                 <th>AUDIT TIME</th>
#                                 <th>Checklist Data</h>
#                                 <th>FEEDBACK</th>
                                
#                             </tr>
#                         """

                        
#                         html += f"""
#                             <tr>
#                                 <td><img src="tick-green-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td>{df['mobile_number'][i]}</td>
#                                 <td>{audit_data.get('auditor',"")}</td>
#                                 <td>{epoch_timestamp}</td>
#                                 <td>Customer livliness check <img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Facematch with AadhaarXML <img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Facematch with Pan<img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Locate Branch<img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Location in India<img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Pan Card<img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Questions<br>Selfie<img src="tick-green-icon.svg" alt="Icon" width="20" height="20"><br>Signature Match<img src="tick-green-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td>{audit_data.get('feedback',"No feedback given")}</td>
                                

                                
#                             </tr>
#                             """

#                         html += """
#                         </table>

#                         </body>
#                         </html>
#                         """
                                                
#                         # Save the generated HTML to a file or use it as needed
#                         # with open("output.html", "w") as html_file:
#                         #     html_file.write(html)

#                         # pdfkit.from_file('output.html', 'a4_2.pdf')
#                     else:
#                         html = """
#                         <!DOCTYPE html>
#                         <html>
#                         <head>
                         
#                             <style>
#                             @page {
#                                 size: 600mm 350mm; /* Landscape, with custom width and height */
#                                 margin: 1cm; /* Adjust margins as needed */
#                             }
                            
#                             body {
#                                 margin: 100px;
#                             }
#                                 table {
#                                 width: 100%;
#                                 border-collapse: collapse;
#                             }

#                             th, td {
#                                 border: 1px solid transparent;
#                                 padding: 8px;
#                                 text-align: center;
#                                 width: 800px;
#                             }
#                             .tbl{
#                                 font-family: "Roboto", "Helvetica", "Arial", sans-serif;
#                             }
                            

#                             th {
#                                 background-color: lavender;
#                             }

#                             /* Remove the border for the right side of cells (vertical lines) */
#                             td {
#                                 border-right: none;
#                             }

#                             tr:nth-child(even) {
#                                 background-color: white;
#                             }

#                             tr:nth-child(odd) {
#                                 background-color: lightgray;
#                             }
#                             </style>
#                         </head>
#                         <body>

#                         <table class="tbl">
#                             <tr>
#                                 <th>AUDIT RESULT</th>
#                                 <th>USER ID</th>
#                                 <th>AUDITOR</th>
#                                 <th>AUDIT TIME</th>
#                                 <th>Checklist Data</h>
#                                 <th>FEEDBACK</th>
                                
#                             </tr>
#                         """


#                         html += f"""
#                             <tr>
#                                 <td><img src="red-x-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td>{df['mobile_number'][i]}</td>
#                                 <td>{audit_data.get('auditor',"")}</td>
#                                 <td></td>
#                                 <td>Customer livliness check <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Facematch with AadhaarXML <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Facematch with Pan <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Locate Branch  <meta name="pdf-page-size" content="A4"><br>Location in India <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Pan Card <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Questions <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Selfie <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Signature Match<img src="red-x-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td><img src="red-x-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td>{audit_data.get('feedback',"No feedback given")}</td>
                                

                                
#                             </tr>
#                             """

#                         html += """
#                         </table>

#                         </body>
#                         </html>
#                         """
                       

#                         # # Save the generated HTML to a file or use it as needed
#                         # with open(f"{folder_name}/{df['mobile_number'][i]}.html", "w") as html_file:
#                         #     html_file.write(html)

                    
#                 else:
#                     html = """
#                         <!DOCTYPE html>
#                         <html>
#                         <head>
                        
#                             <style>
#                             @page {
#                                 size: 600mm 350mm; /* Landscape, with custom width and height */
#                                 margin: 1cm; /* Adjust margins as needed */
#                             }
                              
#                             body {
#                                 margin: 100px;
#                             }
                            
#                                 table {
#                                 width: 100%;
#                                 border-collapse: collapse;
#                             }

#                             th, td {
#                                 border: 1px solid transparent;
#                                 padding: 8px;
#                                 text-align: center;
#                                 width: 800px;
#                             }
#                             .tbl{
#                                 font-family: "Roboto", "Helvetica", "Arial", sans-serif;
#                             }
                            

#                             th {
#                                 background-color: lavender;
#                             }

#                             /* Remove the border for the right side of cells (vertical lines) */
#                             td {
#                                 border-right: none;
#                             }

#                             tr:nth-child(even) {
#                                 background-color: white;
#                             }

#                             tr:nth-child(odd) {
#                                 background-color: lightgray;
#                             }
#                             </style>
#                         </head>
#                         <body>

#                         <table class="tbl">
#                             <tr>
#                                 <th>AUDIT RESULT</th>
#                                 <th>USER ID</th>
#                                 <th>AUDITOR</th>
#                                 <th>AUDIT TIME</th>
#                                 <th>Checklist Data</h>
#                                 <th>FEEDBACK</th>
                                
#                             </tr>
#                         """


#                     html += f"""
#                             <tr>
#                                 <td><img src="red-x-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td>{df['mobile_number'][i]}</td>
#                                 <td></td>
#                                 <td></td>
#                                 <td>Customer livliness check <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Facematch with AadhaarXML <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Facematch with Pan <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Locate Branch <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Location in India <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Pan Card <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Questions <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Selfie <img src="red-x-icon.svg" alt="Icon" width="20" height="20"><br>Signature Match <img src="red-x-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td><img src="red-x-icon.svg" alt="Icon" width="20" height="20"></td>
#                                 <td>No feedback given</td>
                                

                                
#                             </tr>
#                             """

#                     html += """
#                         </table>

#                         </body>
#                         </html>
#                         """
                    
#                         # Save the generated HTML to a file or use it as needed
#                     # with open(f"{folder_name}/{df['mobile_number'][i]}.html", "w") as html_file:
#                     #     html_file.write(html)
#                 with open("my_html_file.html", "w") as file:
#                     file.write(html)

#                 # Convert the local HTML file to PDF
#                 # pdfkit.from_file("my_html_file.html", "a4_2.pdf")
#                 # HTML(string=html).write_pdf("a4_2.pdf")
#                 page_width = 2560  # 2560 pixels
#                 page_height = 1600  # 1600 pixels

#                 # Generate the PDF with the specified page size
#                 pdf_options = {
#                     'page-size': f'{page_width}x{page_height}',
#                     'margin-top': '0mm',  # Set margins to zero for consistency
#                     'margin-right': '0mm',
#                     'margin-bottom': '0mm',
#                     'margin-left': '0mm',
#                 }
#                 with open("pdf2.pdf", "wb") as file2:
#                     pisa.CreatePDF(html, dest=file2, pdf_options=pdf_options)
                
#                 fillpdfs.get_coordinate_map('Admin _ Central bank of India.pdf', 'template.pdf')
                

#                 try:
#                     response = s3.get_object(Bucket=bucket_name, Key=second_pdf)

#                     # Get the contents of the object
#                     # object_content = response['Body'].read()
#                     with open("pdf3.pdf",'wb') as file3:
#                         file3.write(response['Body'].read())

                    
#                     # object = object_content.decode('utf-8') # Assuming it's a text-based file
#                     # obj = json.loads(object)
                    
#                 except Exception as e:
#                     # Handle exceptions if the object retrieval fails
#                     print(e)
                
#                 with open('pdf1.pdf', 'rb') as file1, open('pdf2.pdf', 'rb') as file2, open('pdf3.pdf', 'rb') as file3:
#                     # page_width = 200.276  # Letter size width in points
#                     # page_height = 300.890
#                     # Create PDF reader objects for each file
#                     pdf_reader1 = PyPDF2.PdfReader(file1)
#                     pdf_reader2 = PyPDF2.PdfReader(file2)
#                     pdf_reader3 = PyPDF2.PdfReader(file3)

#                     # Create a PDF writer object to write the merged PDF
#                     pdf_writer = PyPDF2.PdfWriter()

#                     # Add pages from the first PDF
#                     for page_num in range(len(pdf_reader1.pages)):
#                         page = pdf_reader1.pages[page_num]
#                         pdf_writer.add_page(page)

#                     # Add pages from the second PDF
#                     for page_num in range(len(pdf_reader2.pages)):
#                         page = pdf_reader2.pages[page_num]
#                         # page.mediabox.lower_left = (0, 0)
#                         # page.mediabox.upper_right = (page_width, page_height)
#                         pdf_writer.add_page(page)

#                     # Add pages from the third PDF
#                     for page_num in range(len(pdf_reader3.pages)):
#                         page = pdf_reader3.pages[page_num]
#                         pdf_writer.add_page(page)

#                     # Save the merged PDF to the output file
#                     output_file_path = f'{folder_name}/{df["mobile_number"][i]}.pdf'  # Replace with your desired output file name
#                     with open(output_file_path, 'wb') as output:
#                         pdf_writer.write(output)


# print(data_lst)