import csv
import os
import shutil
import re
from sec_edgar_downloader import Downloader


def load_cik_pairs(filename):
    cik_dict = {}

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            symbol, cik = row
            cik_dict[symbol] = cik

    return cik_dict


def process_reports(form_types, symbols, start_date, root_folder):
    cik_pairs = load_cik_pairs('./updaters/cik.csv')
    dl = Downloader()
    for form_type in form_types:
        for symbol in symbols:
            # Download reports
            cik = cik_pairs[symbol]
            full_cik = '0'*(10-len(cik))+cik
            dl.get(form_type, cik, after=start_date)

            folder_path = f'./sec-edgar-filings/{full_cik}/{form_type}'

            # Check if the folder_path exists before proceeding
            if os.path.exists(folder_path):
                for folder_name in os.listdir(folder_path):
                    txt_file = os.path.join(
                        folder_path, folder_name, 'full-submission.txt')
                    html_file = os.path.join(
                        folder_path, folder_name, 'filing-details.html')

                    # Check if the txt_file exists before proceeding
                    if os.path.exists(txt_file):
                        with open(txt_file, 'r') as file:
                            txt = file.read()

                            # Get updated_filename and report_date
                            cik_pattern = r"CENTRAL INDEX KEY:\s*0*(\d+)"
                            cik = re.search(cik_pattern, txt)
                            cik = cik.group(1) if cik else None

                            accession_pattern = r"ACCESSION NUMBER:\s*(0*[\d-]+)"
                            accession = re.search(accession_pattern, txt)
                            accession = accession.group(1).replace(
                                '-', '') if accession else None

                            filename_pattern = r"<FILENAME>([\w\d_-]+\.htm)"
                            filename = re.search(filename_pattern, txt)
                            filename = filename.group(1) if filename else None

                            updated_filename = f"{cik},{accession},{filename}"

                            report_date_pattern = r"CONFORMED PERIOD OF REPORT:\s*(\d+)"
                            report_date = re.search(report_date_pattern, txt)
                            report_date = report_date.group(
                                1) if report_date else None

                    # Check if the html_file exists before proceeding
                    if os.path.exists(html_file):
                        # Copy and rename html file
                        new_folder = f'{root_folder}/EDGAR/{symbol}/{form_type}/{report_date}'
                        os.makedirs(new_folder, exist_ok=True)
                        shutil.copy(html_file, os.path.join(
                            new_folder, f"{updated_filename}"))

                    # Check if the folder exists before proceeding
                    if os.path.exists(os.path.join(folder_path, folder_name)):
                        # Delete original folder
                        shutil.rmtree(os.path.join(folder_path, folder_name))

                    print(f"Successfully processed {new_folder}.")
            else:
                print(f"Folder path {folder_path} does not exist. Skipped.")
