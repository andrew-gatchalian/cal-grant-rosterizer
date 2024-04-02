import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import re
import csv
import pandas as pd
from tkinter import messagebox
import datetime
import sys
import os

# get the path to the directory where PyInstaller extracted the files
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()

# load the logo image
logo_path = os.path.join(bundle_dir, "logo.png")
logo = tk.PhotoImage(file=logo_path)

# create a label with the logo
logo_label = tk.Label(root, image=logo, width=100, height=63)
logo_label.pack()

#100x50 logo

# set the window title and size
root.title("File Selection")
root.geometry("500x300")

# initialize variables to hold file paths
txt_file_path = ""
csv_file_path = ""

def select_file(file_type):
    global txt_file_path, csv_file_path
    # open the file dialog to select a file of the specified type
    file_path = filedialog.askopenfilename(
        title=f"Select {file_type.upper()} file",
        filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}"), ("All Files", "*.*")]
    )
    if file_path:
        if file_type == "txt":
            txt_file_path = file_path
            txt_label.config(text=f"Selected {file_type} file: {txt_file_path}")
        elif file_type == "csv":
            csv_file_path = file_path
            csv_label.config(text=f"Selected {file_type} file: {csv_file_path}")

# create the text file selection button
text_button = tk.Button(root, text="Select Cal Grant Roster (.txt)", command=lambda: select_file("txt"))
text_button.pack(pady=10)

# create a label to show the selected text file path
txt_label = tk.Label(root, text="")
txt_label.pack(pady=5)

# create the CSV file selection button
csv_button = tk.Button(root, text="Select Salesforce Data (.csv)", command=lambda: select_file("csv"))
csv_button.pack(pady=10)

# create a label to show the selected CSV file path
csv_label = tk.Label(root, text="")
csv_label.pack(pady=5)

# create a progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")

# create the label for the copyright notice
copyright_label = tk.Label(root, text="Copyright © 2023 Andrew Gatchalian", font=("Arial", 8))

# pack the label onto the window
copyright_label.pack(side="bottom", pady=5)

def return_ssn(txt_file_path):
    # Open the input file
    with open(txt_file_path, "r") as input_file:

        # Read in the contents of the file
        contents = input_file.read()

        # Use a regular expression to find all matches
        pattern = re.compile(r"\d{9}")
        ssn = pattern.findall(contents)

        # Use a regular expression to find all grant IDs
        pattern = re.compile(r"[A-Z]\d{8}")
        grant_ids = pattern.findall(contents)

        return ssn, grant_ids
    
def return_ssn_csv(txt_file_path):
    # Open the input file
    with open(txt_file_path, "r") as input_file:

        # Read in the contents of the file
        contents = input_file.read()

        # Use a regular expression to find all matches
        pattern = re.compile(r"\d{9}")
        ssn = pattern.findall(contents)

        # Use a regular expression to find all grant IDs
        pattern = re.compile(r"[A-Z]\d{8}")
        grant_ids = pattern.findall(contents)

        # Get current date and time MM-DD-YY
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d") + "_Cal_Grant_Roster_SSN.csv"

        # Allow user to select file path
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 initialfile=filename,
                                                 filetypes=[("CSV Files", "*.csv")])
        if not file_path:  # user cancelled the dialog
            return

        # Export matches to a CSV file
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["SSN", "Grant ID"])
            for match, grant_id in zip(ssn, grant_ids):
                writer.writerow([match, grant_id])

def merge(csv_file_path):
    #SSN dataframe
    ssn_list, grant_ids_list = return_ssn(txt_file_path)
    return_ssn_df = pd.DataFrame({'SSN':ssn_list, 'Grant ID':grant_ids_list})

    # Convert the SSN column to a float data type
    return_ssn_df['SSN'] = return_ssn_df['SSN'].astype(float)

    # Salesforce active students dataframe
    salesforce_df = pd.read_csv(csv_file_path, encoding='latin1')

    # Keep SSN float64, convert Colleague ID column to string type and clean fields
    salesforce_df['SSN'] = salesforce_df['SSN']
    salesforce_df['Colleague ID'] = salesforce_df['Colleague ID'].astype(str).str.zfill(7)

    # Merge the two dataframes based on the "SSN" column
    merged_df = pd.merge(return_ssn_df, salesforce_df, on='SSN', how='left', indicator=True)
    
    #Separate unmatched rows into a separate dataframe
    merged_df['_merge'] = merged_df['_merge'].replace({'left_only': 'Not Found', 'both': 'Ready to Award'})
    unmatched_df = merged_df[merged_df['_merge'] == 'Not Found']
    matched_df = merged_df[merged_df['_merge'] == 'Ready to Award']

    # Concatenate matched and unmatched rows into a single dataframe
    combined_df = pd.concat([matched_df, unmatched_df])

    # Reorder the columns in the combined dataframe
    combined_df = combined_df[['Colleague ID','Name','SSN','Grant ID'] + [col for col in combined_df.columns if col not in ['SSN', 'Colleague ID', 'Name', 'Grant ID']]]

    # Get current date and time MM-DD-YY
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d") + "_Cal_Grant_Roster_FULL.csv"

    # Allow user to select file path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialfile=filename,
                                                filetypes=[("CSV Files", "*.csv")])
    if not file_path:  # user cancelled the dialog
        return

    # Write the combined dataframe to a new CSV file
    combined_df.to_csv(file_path, index=False)

def run_scripts():
    # check if both files have been selected
    if txt_file_path and csv_file_path:
        progress.pack(pady=10)
        # run the function return_ssn
        return_ssn(txt_file_path)
        progress["value"] = 50
        root.update_idletasks()
        # run the function merge
        merge(csv_file_path)
        progress["value"] = 100
        root.update_idletasks()
        print("Scripts completed successfully.")
        # show message box when root is destroyed
        messagebox.showinfo("Complete", "Scripts completed successfully.")
        #Close
    
    elif txt_file_path:
        # run the function return_ssn
        return_ssn_csv(txt_file_path)
        root.update_idletasks()
        print("Scripts completed successfully.")
        # show message box when root is destroyed
        messagebox.showinfo("Complete", "Scripts completed successfully.")
        #Close

    else:
        print("Please select both files before running the scripts.")

# create the run scripts button
run_button = tk.Button(root, text="Run Scripts", command=run_scripts)
run_button.pack(pady=10)

root.mainloop()