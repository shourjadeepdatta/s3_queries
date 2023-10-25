import re
import csv
from datetime import datetime

def filter_logs_to_csv(log_file_path, date_filter, output_csv_name):
    pattern = r'(\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(.*?)\]\s\"(OPTIONS|GET|POST|PUT|DELETE)\s(.*?)/(\d+)/(\w+)\s(.*?)\"\s(\d+)\s(\d+)\s\"(.*?)\"\s\"(.*?)\"'
    
    start_date = datetime.strptime(date_filter[0], "%d/%b/%Y")
    end_date = datetime.strptime(date_filter[1], "%d/%b/%Y")
    
    with open(output_csv_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['IP', 'Timestamp', 'Method', 'API', 'Mobile Number', 'Protocol', 'Status Code', 'Response Size', 'Referrer', 'User-Agent'])
        
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                match = re.search(pattern, line)
                if match:
                    log_date_str = match.group(2).split(":")[0]
                    log_date = datetime.strptime(log_date_str, "%d/%b/%Y")
                    
                    if start_date <= log_date <= end_date:
                        csv_writer.writerow([
                            match.group(1),
                            match.group(2),
                            match.group(3),
                            match.group(4),
                            match.group(5),
                            match.group(6),
                            match.group(7),
                            match.group(8),
                            match.group(9),
                            match.group(10),
                            match.group(11)
                        ])

# Example usage:
filter_logs_to_csv("access.log", ("13/Jul/2023", "26/Sep/2023"), "13jul_26sep_logs.csv")
