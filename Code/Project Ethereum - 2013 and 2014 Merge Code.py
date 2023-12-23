import csv
import glob
csv_directory = "/Users/alinachen/Documents/Research/Jiasun Li and Mariia Petryk/2013-2014/" # Change Location
csv_pattern = "*.csv"
csv_files = glob.glob(csv_directory + csv_pattern)
combined_csv = "AllData20132014.csv"
for i, csv_file in enumerate(csv_files):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        if i != 0:
            next(csv_reader)
        with open(combined_csv, 'a', newline='') as combined_file:
            csv_writer = csv.writer(combined_file)
            for row in csv_reader:
                csv_writer.writerow(row)