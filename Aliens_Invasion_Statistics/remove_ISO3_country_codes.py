import csv

country_codes_file = 'countrycode.org.csv'
file = open(country_codes_file)
reader = csv.reader(file)
data = []
for row in reader:
    row[0] = row[0].strip()
    row[1] = row[1].split('/')[0].strip()
    data.append(row)


writer = csv.writer(open('countrycode.org.csv', "w"), lineterminator='\n')
writer.writerows(data)
