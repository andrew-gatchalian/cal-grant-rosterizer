## Cal Grant Rosterizer
                                                                 
ROSTERIZER_1.0 - README.txt
Welcome to Rosterizer_1.0! This is a simple executable file that helps you automate the process of cleaning a TXT file, merges them with data, and exports the results to a CSV

Process
Rosterizer_1.0 takes in information from a TXT file (Cal Grant Roster) and stores the SSN and Grant ID to a dataframe. The user can run a script to generate a CSV file with all SSNs listed.
The user may also select another seperate CSV file (Salesforce) containing all FAFSAs available in system. The user can run a script that merges the Cal Grant Roster and Salesforce data to
generate a CSV list of students that are "Ready to Award" or (if not in system yet) "Not Found".

Installation
There is no need for installation. Simply double-click the "rosterizer_1.0.exe" file to run the program.

Usage
To use Rosterizer_1.0, follow these simple steps:

	1. Click the "Select Cal Grant Roster (.txt)" button to select the Cal Grant Roster text file.
		a. *To only pull SSN click "Run Scripts"
		b. CSV is named:(YEAR)(MONTH)(DAY)_Cal_Grant_Roster_SSN
		c. Select where to save file

	2. To link Cal Grant Roster SSN to Colleague ID + Name... 
		a. Download the 2X-2X All FAFSA Data report from Salesforce.

	3. Click the "Select Salesforce Data (.csv)" button to select the Salesforce data CSV file.

	4. Click the "Run Scripts" button to merge both data sets and export a CSV file.

	5. CSV is named: (YEAR)(MONTH)(DAY)_Cal_Grant_Roster_FULL
		a. Select where to save file

Disclaimer
Rosterizer_1.0 is a simple exe file made to clean Cal Grant Rosters from the California Student Aid Commision (CSAC) WebGrants website. 
CSV files are specifically Salesforce reports from Fresno Pacific University, but can be connected with any database using SSN as a field.
Changes to the code will need to be made to generate different fields.

Enjoy! Thank you for using Rosterizer_1.0!



