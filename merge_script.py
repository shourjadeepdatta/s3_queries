import PyPDF2
import boto3
import pandas as pd
import os
import re
import json
from datetime import datetime
# import fitz
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.pdfgen import canvas
import shutil


endpoint_url = "https://mio.vkyc.cbi.prod.getkwikid.com"


s3 = boto3.client('s3', aws_access_key_id = "minio",
                  aws_secret_access_key="minio@123",
                  endpoint_url=endpoint_url, verify=False)

bucket_name = 'kwikid'
lst = []
folder_name = 'merged'
file_path = 'daily_2023-09-20.xlsx'
pdf_files = ['a4_1.pdf', 'a4_2.pdf', 'a4_3.pdf']
columns_to_read = ['mobile_number','session_id']
df = pd.read_excel(file_path,sheet_name='Account Data' ,usecols=columns_to_read)
print(len(df['mobile_number']))
os.makedirs(folder_name, exist_ok=True)
dpi = 500

for i in range(2):


# for i in range(len(df['mobile_number'])):
    
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

                    

                    # pdf_file = "pdf1.pdf"

                    # # Create a new PDF with A4 page size
                    # output_pdf = fitz.open()

                    # # Set A4 page dimensions (595.276 x 841.890 points, approximately 8.27 x 11.69 inches)
                    # page_width, page_height = 595.276, 841.890

                    # # Iterate through the input PDF and copy pages to the new PDF
                    # pdf_document = fitz.open(pdf_file)
                    # for page_num in range(len(pdf_document)):
                    #     page = pdf_document[page_num]
                        
                    #     # Create a new page with A4 dimensions
                    #     new_page = output_pdf.new_page(width=page_width, height=page_height)
                        
                    #     # Render the original page onto the new page
                    #     page_pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), dpi=dpi)  # Render the page as an image
                    #     new_page.insert_image(fitz.Rect(0, 0, page_width, page_height), pixmap=page_pix)
                        
                    # # Save the new PDF with A4 page size
                    # output_pdf.save("a4_1.pdf")
                    # output_pdf.close()
                    
                    # object = object_content.decode('utf-8') # Assuming it's a text-based file
                    # obj = json.loads(object)
                    
                except Exception as e:
                    # Handle exceptions if the object retrieval fails
                    print(e)
                
                try:
                    response = s3.get_object(Bucket=bucket_name, Key=second_pdf)

                    # Get the contents of the object
                    # object_content = response['Body'].read()
                    with open("pdf2.pdf",'wb') as file2:
                        file2.write(response['Body'].read())

                    
                    # pdf_file = "pdf2.pdf"

                    # output_pdf = fitz.open()

                    # # Set A4 page dimensions (595.276 x 841.890 points, approximately 8.27 x 11.69 inches)
                    # page_width, page_height = 595.276, 841.890

                    # # Iterate through the input PDF and copy pages to the new PDF
                    # pdf_document = fitz.open(pdf_file)
                    # for page_num in range(len(pdf_document)):
                    #     page = pdf_document[page_num]
                        
                    #     # Create a new page with A4 dimensions
                    #     new_page = output_pdf.new_page(width=page_width, height=page_height)
                        
                    #     # Render the original page onto the new page
                    #     page_pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), dpi=dpi)  # Render the page as an image
                    #     new_page.insert_image(fitz.Rect(0, 0, page_width, page_height), pixmap=page_pix)
                        
                    # # Save the new PDF with A4 page size
                    # output_pdf.save("a4_2.pdf")
                    # output_pdf.close()

                    
                    # object = object_content.decode('utf-8') # Assuming it's a text-based file
                    # obj = json.loads(object)
                    
                except Exception as e:
                    # Handle exceptions if the object retrieval fails
                    print(e)


                with open('pdf1.pdf', 'rb') as file1, open('pdf2.pdf', 'rb') as file2:
                    # Create PDF reader objects
                    pdf_reader1 = PyPDF2.PdfReader(file1)
                    pdf_reader2 = PyPDF2.PdfReader(file2)

                    # Create a PDF writer object to write the merged PDF
                    pdf_writer = PyPDF2.PdfWriter()

                    # Add pages from the first PDF
                    for page_num in range(len(pdf_reader1.pages)):
                        page = pdf_reader1.pages[page_num]
                        pdf_writer.add_page(page)


                    # Add pages from the second PDF
                    for page_num in range(len(pdf_reader2.pages)):
                        page = pdf_reader2.pages[page_num]
                        pdf_writer.add_page(page)

                    # Save the merged PDF to the output file
                    output_file_path = f'{df["mobile_number"][i]}.pdf'
                    output_path = os.path.join(folder_name,output_file_path)
                    print(output_path)
                    # output_file_path = 'merged.pdf'
                    with open(output_path, 'wb') as output:
                        pdf_writer.write(output)

# os.remove('a4_1.pdf')
# os.remove('a4_2.pdf')
os.remove('pdf1.pdf')
os.remove('pdf2.pdf')