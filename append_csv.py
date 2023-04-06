# Append row to existing CSV file
import csv

# 'a' - append mode
csv_file = open('books.csv', 'a')

writer = csv.writer(csv_file, delimiter=';')
writer.writerow(['New book'])

csv_file.close()


# CSV dict writer
import csv

csv_file = open('books.csv', 'a')

fieldnames = ['name', 'pages_count', 'authors', 'country']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
writer.writerow({'name': 'New book', 'pages_count': 100, 'authors': 'Author', 'country': 'Country'})
