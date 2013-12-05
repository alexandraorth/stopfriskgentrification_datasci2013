import csv

reader=csv.reader(open("race.csv","rb"),delimiter='\t')
data=list(reader)
race_data = {}
for i in range(1,len(data)):
	row = data[i]
	row = row[0].split(',')
	print row
	precint = int(row[2].strip())
	race = row[1].replace('"','')
	count = row[3]
	try:
		throwaway = race_data[precint]
	except:
		race_data[precint] = {}
	try:
		race_data[precint][race] = int(count)
	except:
		pass
print race_data
