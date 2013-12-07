# Khalid Richards
# November 21, 2013

# baseline.py
# Extracting data for the baseline and turning it into a nice CSV

import csv
import the_strings, the_constants

# Notes: BNX = Bronx, MNH = Manhattan, QUN = Queens, BRK = Brooklyn, SI = Staten Island

num_of_cds = {"BNX":12, "BRK":18, "MNH":12, "QUN":14, "SI":3}
start_pos = {"BNX":1, "BRK":41, "MNH":113, "QUN": 153, "SI":209} #for lots of the 2010 data
names_of_boroughs = {"BNX": "Bronx", "BRK":"Brooklyn", "MNH":"Manhattan", "QUN":"Queens", "SI":"Staten Island"}
bnx_cd_info = {}
mnh_cd_info = {}
qun_cd_info = {}
brk_cd_info = {}
si_cd_info = {}
cd_info = {"BNX":bnx_cd_info, "BRK":brk_cd_info, "MNH":mnh_cd_info, "QUN":qun_cd_info, "SI":si_cd_info}

def slope(after, before):
	return (after - before) / 10.0

def pct_change(after, before):
	print after
	print before
	return (after - before) / float(before)

def index(value, baseline):
	if value > baseline:
		return 1
	elif value >= (0.9 * baseline) or value <= (1.1 * baseline):
		return -1
	else:
		return 0

def init_dicts():
	for k,v in num_of_cds.iteritems():
		for i in range(v):
			if k == "BNX":
				bnx_cd_info[i+1] = []
			elif k == "BRK":
				brk_cd_info[i+1] = []
			elif k == "MNH":
				mnh_cd_info[i+1] = []
			elif k == "QUN":
				qun_cd_info[i+1] = []
			else:
				si_cd_info[i+1] = []

def bnx_aux_parse(dictionary, start_pos, row):
	dictionary[1].append(comma_int(row[start_pos]))
	dictionary[2].append(comma_int(row[start_pos]))
	dictionary[3].append(comma_int(row[start_pos + 4]))
	dictionary[6].append(comma_int(row[start_pos + 4]))
	dictionary[4].append(comma_int(row[start_pos + 8]))
	dictionary[5].append(comma_int(row[start_pos + 12]))
	for j in range(7, 13):
		dictionary[j].append(comma_int(row[start_pos + 4 * (j-3)]))

def mnh_aux_parse(dictionary, start_pos, row):
	# print "IN MNH AUX PARSE" 
	dictionary[1].append(comma_int(row[start_pos]))
	dictionary[2].append(comma_int(row[start_pos]))
	dictionary[3].append(comma_int(row[start_pos + 4]))
	dictionary[6].append(comma_int(row[start_pos + 4]))
	dictionary[4].append(comma_int(row[start_pos + 8]))
	dictionary[5].append(comma_int(row[start_pos + 12]))
	for j in range(7, 13):
		dictionary[j].append(comma_int(row[start_pos + 4 * (j-3)]))

def demo_2000_parse(cursor, dictionary, reader, key):
	BEGINNING = 0
	POPULATION_TOTAL_LINE = 2
	POPULATION_WHITE_NONHISPANIC = 3
	POPULATION_BLACK_NONHISPANIC = 4
	POPULATION_HISPANIC = 8
	RENTER_OCCUPIED = 46
	OWNER_OCCUPIED = 47
	SKIP = 60

	district = 0
	ctr = 0

	while ctr != cursor:
		ctr += 1
		g = reader.next()
		# print g

	print "CURRENT BOROUGH: " + key
	print "CURSOR VALUE: " + str(cursor)
	while(ctr < cursor + num_of_cds[key] * 60): #End of index
		row = reader.next()
		# print str(ctr) + " : "
		# print row
		if ctr % SKIP == BEGINNING:
			district += 1
		elif ctr % SKIP == POPULATION_TOTAL_LINE:
			print "ADDING STUFF FROM THIS ROW"
			print row
			dictionary[district].append(comma_int(row[0].split()[2]))
		elif ctr % SKIP in (POPULATION_WHITE_NONHISPANIC, POPULATION_BLACK_NONHISPANIC, POPULATION_HISPANIC, RENTER_OCCUPIED, OWNER_OCCUPIED):
			if row[4] != '':
				print "ADDING STUFF FROM THIS ROW"
				print row
				dictionary[district].append(comma_int(row[4]))
			else:
				print "ADDING STUFF FROM THIS ROW"
				print row
				dictionary[district].append(comma_int(row[3]))
		ctr += 1


def demo_2010_parse(reader, dictionary, dict_tag, start_index):
	TOTAL_POPULATION = 35
	WHITE = 39
	BLACK = 40
	HISPANIC = 75

	DESIRED_INDEX = start_index
	i = 0
	while(i <= 76):
		row = reader.next()
		if i in (TOTAL_POPULATION, WHITE, BLACK, HISPANIC):
			if dict_tag == "BNX":
				dictionary[1].append(comma_int(row[DESIRED_INDEX]))
				dictionary[2].append(comma_int(row[DESIRED_INDEX]))
				dictionary[3].append(comma_int(row[DESIRED_INDEX + 4]))
				dictionary[6].append(comma_int(row[DESIRED_INDEX + 4]))
				dictionary[4].append(comma_int(row[DESIRED_INDEX + 8]))
				dictionary[5].append(comma_int(row[DESIRED_INDEX + 12]))
				for j in range(7, 13):
					dictionary[j].append(comma_int(row[DESIRED_INDEX + 4 * (j-3)]))

			elif dict_tag == "MNH":
				dictionary[1].append(comma_int(row[DESIRED_INDEX]))
				dictionary[2].append(comma_int(row[DESIRED_INDEX]))
				dictionary[4].append(comma_int(row[DESIRED_INDEX + 4]))
				dictionary[5].append(comma_int(row[DESIRED_INDEX + 4]))
				dictionary[3].append(comma_int(row[DESIRED_INDEX + 8]))
				for j in range(6, 13):
					dictionary[j].append(comma_int(row[DESIRED_INDEX + 4 * (j-3)]))

			else:
				for j in range(1, num_of_cds[dict_tag] + 1):
					dictionary[j].append(comma_int(row[DESIRED_INDEX + 4 * (j-1)]))
		i +=1

def demo_2010_aux_parse(cd_tag, dictionary, start_pos):
	with open('csv_files/housing_2010.csv', 'rb') as housing_info:
		reader = csv.reader(housing_info)
		RENTERS = 57
		OWNERS = 58
		DATA = start_pos
		i = 1
		for row in reader:
			if i == RENTERS or i == OWNERS:
				if cd_tag == "BNX":
					dictionary[1].append(comma_int(row[DATA]))
					dictionary[2].append(comma_int(row[DATA]))
					dictionary[3].append(comma_int(row[DATA + 4]))
					dictionary[6].append(comma_int(row[DATA + 4]))
					dictionary[4].append(comma_int(row[DATA + 8]))
					dictionary[5].append(comma_int(row[DATA + 12]))
					for j in range(7,13):
						dictionary[j].append(comma_int(row[DATA + 4 * (j-3)]))

				elif cd_tag == "MNH":
					dictionary[1].append(comma_int(row[DATA]))
					dictionary[2].append(comma_int(row[DATA]))
					dictionary[4].append(comma_int(row[DATA + 4]))
					dictionary[5].append(comma_int(row[DATA + 4]))
					dictionary[3].append(comma_int(row[DATA + 8]))
					for j in range(6, 13):
						dictionary[j].append(comma_int(row[DATA + 4 *(j-3)]))
				else:
					for j in range(1,num_of_cds[cd_tag] + 1):
						dictionary[j].append(comma_int(row[DATA + 4 * (j-1)]))
			i += 1


# Adds the 2010 and 2011 racial info + home ownership info
def add_demographic_info(file2000, file2010):
	with open(file2000, 'rb') as demo_2000:
		with open(file2010, 'rb') as demo_2010:
			reader_old = csv.reader(demo_2000)
			reader_new = csv.reader(demo_2010)
			startings = {"BNX": 0, "BRK": 720, "MNH":1800, "QUN": 2520, "SI": 3360}
			#Add the 2000 info
			i = 1
			print "IN DEMOGRAPHIC INFO\n\n\n"
			for k,v in cd_info.iteritems():
				demo_2000.seek(0)
				demo_2010.seek(0)
				m = start_pos[k]
				cursor = startings[k]
				demo_2000_parse(cursor, v, reader_old, k)
				demo_2010_parse(reader_new, v, k, m)
				demo_2010_aux_parse(k, v, m)
				print k
				print v
			#Add the 2010 info
			#Note: BNX CDs 1&2, 3&6, MNH CDs 1&2, 4&5

# Pop>25: 2000 (Col 2) | 2010 (Row 72)
# <9th grade: 2000 (Cols 3 + 6) | 2010 (Row 73)
# HS, no dip: 2000 (Cols 7 + 10) | 2010 (Row 74)
# HS, dip: 2000 (Col 12) | 2010 (Row 75)
# Bachelor's Degree 2000 (Col 18) | 2010 (Row 78)
# Grad Degree 2000 (Col 19-21)| 2010 (Row 79)

def edu_2000_parse(reader):
	for row in reader:
		if(row[0].find("Bronx") >= 0):
			edu_2000_helper(bnx_cd_info, row)
		elif row[0].find("Brooklyn") >= 0:
			edu_2000_helper(brk_cd_info, row)
		elif row[0].find("Manhattan") >= 0:
			edu_2000_helper(mnh_cd_info, row)
		elif row[0].find("Queens") >= 0:
			edu_2000_helper(qun_cd_info, row)
		elif row[0].find("Staten Island") >= 0:
			edu_2000_helper(si_cd_info, row)

def comma_int(str_to_int):
	h = str_to_int.replace('+', "")
	h = h.replace('$', "")
	h = h.replace(',', "")
	return int(h)

def edu_2000_helper(dictionary, row):
	cd = 0
	if len(row[0].split()[1]) > 2:
		cd = comma_int(row[0].split()[2])
	else:
		cd = comma_int(row[0].split()[1])
	dictionary[cd].append(comma_int(row[1]))
	dictionary[cd].append(sum([comma_int(row[2]), comma_int(row[3]), comma_int(row[4]), comma_int(row[5])]))
	dictionary[cd].append(sum([comma_int(row[6]), comma_int(row[7]), comma_int(row[8]), comma_int(row[9])]))
	dictionary[cd].append(comma_int(row[11]))
	dictionary[cd].append(comma_int(row[17]))
	dictionary[cd].append(sum([comma_int(row[18]), comma_int(row[19]), comma_int(row[20])]))


def edu_2010_parse(reader, dictionary, cd_tag, start_pos):
	BELOW_NINTH = 73
	HS_NO_DIP = 74
	HS_DIP = 75
	BS_DEG = 78
	GRAD_DEG = 79

	i = 1

	for row in reader:
		if i in (BELOW_NINTH, HS_NO_DIP, HS_DIP, BS_DEG, GRAD_DEG):
			if cd_tag == "BNX":
				dictionary[1].append(comma_int(row[start_pos]))
				dictionary[2].append(comma_int(row[start_pos]))
				dictionary[3].append(comma_int(row[start_pos + 4]))
				dictionary[6].append(comma_int(row[start_pos + 4]))
				dictionary[4].append(comma_int(row[start_pos + 8]))
				dictionary[5].append(comma_int(row[start_pos + 12]))
				for j in range(7, 13):
					dictionary[j].append(comma_int(row[start_pos + 4 * (j-3)]))
			elif cd_tag == "MNH":
				dictionary[1].append(comma_int(row[start_pos]))
				dictionary[2].append(comma_int(row[start_pos]))
				dictionary[4].append(comma_int(row[start_pos + 4]))
				dictionary[5].append(comma_int(row[start_pos + 4]))
				dictionary[3].append(comma_int(row[start_pos + 8]))
				for j in range(6, 13):
					dictionary[j].append(comma_int(row[start_pos + 4 * (j-3)]))
			else:
				for j in range(1, num_of_cds[cd_tag] + 1):
					dictionary[j].append(comma_int(row[start_pos + 4 * (j-1)]))
		i += 1

def add_edu_info(file2000, file2010):
	with open(file2000, 'rb') as edu_2000:
		with open(file2010, 'rb') as edu_2010:
			reader_old = csv.reader(edu_2000)
			reader_new = csv.reader(edu_2010)

			for k,v in cd_info.iteritems():
				edu_2010.seek(0)
				edu_2000_parse(reader_old)
				edu_2010_parse(reader_new, v, k, start_pos[k])
				print "IN EDU INFO\n"
				print k
				print v

def add_occ_2000_parse(reader, key, start_pos):
	#logic
	TOTAL_EMPLOYMENT = 1
	MANAGEMENT = 2
	PER_CAPITA = 9

	dictionary = cd_info[key]
	if key != "BNX":
		start_pos += 1

	i = 0

	for row in reader:
		if i in (TOTAL_EMPLOYMENT, MANAGEMENT, PER_CAPITA):
			for j in range(1, num_of_cds[key] + 1):
				print row[start_pos + (j-1)]
				dictionary[j].append(comma_int(row[start_pos + (j-1)]))
		i += 1

def add_occ_2000_aux_parse(cd_tag, dictionary):
	start_positions = {"BNX": 7, "BRK":20, "MNH":39, "QUN":52, "SI":67}
	with open('csv_files/med_house_income_2000.csv', 'rb') as f:
		reader = csv.reader(f)
		i = 0
		j = 1
		while i <= start_positions[cd_tag] + num_of_cds[cd_tag] -1:
			row = reader.next()
			if i >= start_positions[cd_tag]:
				dictionary[j].append(comma_int(row[18]))
				j += 1
			i += 1


def add_occ_2010_parse(reader, dictionary, cd_tag, start_pos):
	TOTAL_EMPLOYMENT = 8
	MANAGEMENT = 36
	MEDIAN_HOUSE_INC = 74
	PER_CAPITA = 100

	i = 1
	for row in reader:
		if i in (TOTAL_EMPLOYMENT,MANAGEMENT, MEDIAN_HOUSE_INC, PER_CAPITA):
			if cd_tag == "BNX":
				bnx_aux_parse(dictionary, start_pos, row)
			elif cd_tag == "MNH":
				mnh_aux_parse(dictionary, start_pos, row)
			else:
				for j in range(1, num_of_cds[cd_tag] + 1):
					dictionary[j].append(comma_int(row[start_pos + 4*(j-1)]))
		i += 1

def add_occ_income_info(file2000, file2010):
	with open(file2000, 'rb') as occ_income_2000:
		with open(file2010, 'rb') as occ_income_2010:
			reader_old = csv.reader(occ_income_2000)
			reader_new = csv.reader(occ_income_2010)
			old_start = 1
			start_positions = {"BNX": 1, "BRK": 13, "MNH":32, "QUN": 45, "SI":60}

			for k,v in cd_info.iteritems():
				occ_income_2000.seek(0)
				occ_income_2010.seek(0)
				add_occ_2000_parse(reader_old, k, start_positions[k])
				add_occ_2000_aux_parse(k,v) #adds the median house income
				add_occ_2010_parse(reader_new, v, k, start_pos[k])
				print "IN ADD_OCC_INCOME INFO"
				print k
				print v

def housing_2000_parse(reader):
	for row in reader:
		if(row[0].find("Bronx") >= 0):
			housing_2000_helper(bnx_cd_info, row)
		elif row[0].find("Brooklyn") >= 0:
			housing_2000_helper(brk_cd_info, row)
		elif row[0].find("Manhattan") >= 0:
			housing_2000_helper(mnh_cd_info, row)
		elif row[0].find("Queens") >= 0:
			housing_2000_helper(qun_cd_info, row)
		elif row[0].find("Staten Island") >= 0:
			housing_2000_helper(si_cd_info, row)

def housing_2000_helper(dictionary, row):
	cd = row[0].split()[1]
	if len(cd) > 2:
		cd = comma_int(row[0].split()[2])
	else:
		cd = comma_int(cd)
	dictionary[cd].append(comma_int(row[1]))
	dictionary[cd].append(comma_int(row[2]))
	dictionary[cd].append(comma_int(row[3]))
	dictionary[cd].append(comma_int(row[4]))

def housing_2010_parse(reader, dictionary, cd_tag, start_pos):
	TOTAL_HOUSING = 25
	LATER_2005 = 26
	BETWEEN_2000_AND_2004 = 27

	i = 1

	for row in reader:
		if i in (TOTAL_HOUSING, LATER_2005, BETWEEN_2000_AND_2004):
			if cd_tag == "BNX":
				bnx_aux_parse(dictionary, start_pos, row)
			elif cd_tag == "MNH":
				mnh_aux_parse(dictionary, start_pos, row)
			else:
				for j in range(1, num_of_cds[cd_tag]+1):
					dictionary[j].append(comma_int(row[start_pos + 4 * (j-1)]))
		i += 1

def add_housing_info(file2000, file2010):
	with open(file2000, 'rb') as housing_2000:
		with open(file2010, 'rb') as housing_2010:
			reader_old = csv.reader(housing_2000)
			reader_new = csv.reader(housing_2010)

			for k,v in cd_info.iteritems():
				housing_2010.seek(0)
				housing_2000_parse(reader_old)
				housing_2010_parse(reader_new, v, k, start_pos[k])
				print "IN HOUSING"
				print k
				print v

def moving_2000_parse(reader):
	for row in reader:
		if(row[0].find("Bronx") >= 0):
			moving_2000_helper(bnx_cd_info, row)
		elif row[0].find("Brooklyn") >= 0:
			moving_2000_helper(brk_cd_info, row)
		elif row[0].find("Manhattan") >= 0:
			moving_2000_helper(mnh_cd_info, row)
		elif row[0].find("Queens") >= 0:
			moving_2000_helper(qun_cd_info, row)
		elif row[0].find("Staten Island") >= 0:
			moving_2000_helper(si_cd_info, row)

def moving_2000_helper(dictionary, row):
	cd = 0
	if len(row[0].split()) > 2:
		cd = comma_int(row[0].split()[2])
	else:
		cd = comma_int(row[0].split()[1])

	dictionary[cd].append(comma_int(row[2]))
	dictionary[cd].append(comma_int(row[3]))
	dictionary[cd].append(comma_int(row[4]))

def moving_2010_parse(reader, dictionary, cd_tag, start_pos):
	TOTAL_MOVING = 62
	MOVED_2005 = 63
	MOVED_2000_TO_2004 = 64

	i = 1

	for row in reader:
		if i in (TOTAL_MOVING, MOVED_2005, MOVED_2000_TO_2004):
			if cd_tag == "BNX":
				bnx_aux_parse(dictionary, start_pos, row)
			elif cd_tag == "MNH":
				mnh_aux_parse(dictionary, start_pos, row)
			else:
				for j in range(1, num_of_cds[cd_tag]+1):
					dictionary[j].append(comma_int(row[start_pos + 4*(j-1)]))
		i += 1

def add_moving_info(file2000, file2010):
	with open(file2000, 'rb') as moving_2000:
		with open(file2010, 'rb') as moving_2010:
			reader_old = csv.reader(moving_2000)
			reader_new = csv.reader(moving_2010)

			for k,v in cd_info.iteritems():
				moving_2010.seek(0)
				moving_2000_parse(reader_old)
				moving_2010_parse(reader_new, v, k, start_pos[k])
				print "IN MOVING"
				print k
				print v

def rent_2000_parse(reader):
	for row in reader:
		if(row[0].find("Bronx") >= 0):
			rent_2000_helper(bnx_cd_info, row)
		elif row[0].find("Brooklyn") >= 0:
			rent_2000_helper(brk_cd_info, row)
		elif row[0].find("Manhattan") >= 0:
			rent_2000_helper(mnh_cd_info, row)
		elif row[0].find("Queens") >= 0:
			rent_2000_helper(qun_cd_info, row)
		elif row[0].find("Staten Isl") >= 0:
			rent_2000_helper(si_cd_info, row)

def rent_2000_helper(dictionary, row):
	#add value before rent
	print row
	cd = row[0].split()
	if len(cd) > 2:
		cd = comma_int(row[0].split()[2])
	else:
		cd = comma_int(row[0].split()[1])
	dictionary[cd].append(comma_int(row[22]))

def rent_2010_parse(reader, dictionary, cd_tag, start_pos):
	MEDIAN_VALUE = 106
	MEDIAN_RENT = 154
	i = 1
	for row in reader:
		if i in (MEDIAN_VALUE, MEDIAN_RENT):
			if cd_tag == "BNX":
				bnx_aux_parse(dictionary, start_pos, row)
			elif cd_tag == "MNH":
				mnh_aux_parse(dictionary, start_pos, row)
			else:
				for j in range(1, num_of_cds[cd_tag]+1):
					dictionary[j].append(comma_int(row[start_pos + 4*(j-1)]))
		i += 1

def add_rent_info(file2000, file2010):
	with open(file2000, 'rb') as rent_2000:
		with open(file2010, 'rb') as rent_2010:
			reader_old = csv.reader(rent_2000)
			reader_new = csv.reader(rent_2010)

			for k,v in cd_info.iteritems():
				rent_2010.seek(0)
				rent_2000_parse(reader_old)
				rent_2010_parse(reader_new, v, k, start_pos[k])
				print "IN RENT"
				print k
				print v

def write_csv():
	columns = ["community_district", "gentrificiation_index(pct_change)", "gentrificiation_index(slope)"]
	calc_columns = ["borough", "pct_change_black", "pct_change_white", "pct_change_renters", "pct_change_education", "pct_change_employment"]
	calc_columns.extend(["pct_change_pci", "pct_change_income", "pct_change_housing", "pct_change_moving", "pct_change_rent"])
	with open(the_strings.WRITE_FILE, 'wb') as f:
		writer = csv.writer(f, delimiter=',')
		with open(the_strings.CALC_FILE, 'wb ') as cf:
			calc_writer = csv.writer(cf, delimiter=',')
			writer.writerow(columns)
			calc_writer.writerow(calc_columns)

			for k,v in cd_info.iteritems():			
				print "\n\n\n\nWRITING CSV\n\n\n"
				print k
				gentrification_index(writer, k, v)
				write_calculation_csv(calc_writer, k, v)

def write_population_csv():
	columns = ["community_district", "population_in_2010"]
	with open(the_strings.POPULATION_FILE, 'wb') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(columns)

		for k,v in cd_info.iteritems():
			borough = names_of_boroughs[k]
			for l,m in v.iteritems():
				name = borough + str(l)
				population = m[6]
				row = [name, population]
				writer.writerow(row)

def get_combined_info(a,b):
	c = []
	for m,n in zip(a,b):
		if m != n:
			c.append(m + n)
		else:
			c.append(m)
	return c

def write_calculation_csv(writer, k, v):
	borough = names_of_boroughs[k]

	if k == "BNX" or k == "MNH":
		special_calc_write(writer, k, v)

	for key in v:
		data = v[key]
		row = []
		row.append(borough + " " + str(key))
		row.append(pct_change(data[8]/float(data[6]), data[2]/float(data[0])))
		row.append(pct_change(data[7]/float(data[6]), data[1]/float(data[0])))

		X1_old = (data[16] + data[17]) / (data[14] + float(data[13]))
		X1_new = (data[22] + data[21]) / (data[19] + float(data[18]))
		row.append(pct_change(data[10], data[4]))
		row.append(pct_change(X1_new, X1_old))

		O1_old = data[24] / float(data[23])
		O1_new = data[28] / float(data[26])
		row.append(pct_change(O1_new, O1_old))

		row.append(pct_change(float(data[30]), data[25]))
		row.append(pct_change(float(data[27]), data[31]))

		H1_old = sum([data[32], data[34], data[35]]) / float(data[32])
		H1_new = (data[36] + data[37]) / float(data[35])
		row.append(pct_change(H1_new, H1_old))

		M1_old = (data[39] + data[40]) / float(data[38])
		M1_new = (data[42] + data[43]) / float(data[41])
		row.append(pct_change(M1_new, M1_old))
		row.append(pct_change(float(data[46]), float(data[44])))

		writer.writerow(row)

def special_calc_write(writer, k, v):
	if k == "BNX":
		#write using BNX rules
		bnx_1_2 = get_combined_info(v[1], v[2])
		bnx_3_6 = get_combined_info(v[3], v[6])

		writer.writerow(special_calcs(bnx_1_2, k, "1&2"))
		writer.writerow(special_calcs(bnx_3_6, k, "3&6"))
		writer.writerow(special_calcs(v[4], k, "4"))
		writer.writerow(special_calcs(v[5], k, "5"))

		for j in range(7, num_of_cds[k] + 1):
			writer.writerow(special_calcs(v[j], k, str(j)))

	elif k == "MNH":
		#write using MNH rules
		bnx_1_2 = get_combined_info(v[1], v[2])
		bnx_4_5 = get_combined_info(v[4], v[5])

		writer.writerow(special_calcs(bnx_1_2, k, "1&2"))
		writer.writerow(special_calcs(bnx_4_5, k, "4&5"))
		writer.writerow(special_calcs(v[3], k, "3"))

		for j in range(6, num_of_cds[k] + 1):
			writer.writerow(special_calcs(v[j], k, str(j)))
	return 1

def special_calcs(data, k, borough_num):
	row = []
	row.append(names_of_boroughs[k] + " " + borough_num)
	row.append(pct_change(data[8]/float(data[6]), data[2]/float(data[0])))
	row.append(pct_change(data[7]/float(data[6]), data[1]/float(data[0])))

	X1_old = (data[16] + data[17]) / (data[14] + float(data[13]))
	X1_new = (data[22] + data[21]) / (data[19] + float(data[18]))
	row.append(pct_change(data[10], data[4]))
	row.append(pct_change(X1_new, X1_old))

	O1_old = data[24] / float(data[23])
	O1_new = data[28] / float(data[26])
	row.append(pct_change(O1_new, O1_old))

	row.append(pct_change(float(data[30]), data[25]))
	row.append(pct_change(float(data[27]), data[31]))

	H1_old = sum([data[32], data[34], data[35]]) / float(data[32])
	H1_new = (data[36] + data[37]) / float(data[35])
	row.append(pct_change(H1_new, H1_old))

	M1_old = (data[39] + data[40]) / float(data[38])
	M1_new = (data[42] + data[43]) / float(data[41])
	row.append(pct_change(M1_new, M1_old))
	row.append(pct_change(float(data[46]), float(data[44])))

	return row


def special_results(data, k, borough_num):
		name = names_of_boroughs[k] + " " +borough_num
		index_pct = 0
		index_slope = 0

		#1. Population Scores
		index_pct += -1 * index(pct_change(data[8]/float(data[6]), data[2]/float(data[0])), the_constants.PCT_CHANGE_BLACK)
		index_pct += index(pct_change(data[7]/float(data[6]), data[1]/float(data[0])), the_constants.PCT_CHANGE_WHITE)
		# index_pct += index(pct_change(data[9], data[3]), the_constants.PCT_CHANGE_HISPANIC)
		index_pct += index(pct_change(data[10], data[4]), the_constants.PCT_CHANGE_RENTERS)

		index_slope += index(slope(data[8], data[2]), the_constants.SLOPE_BLACK)
		index_slope += index(slope(data[7], data[1]), the_constants.SLOPE_WHITE)
		# index_slope += index(slope(data[9], data[3]), the_constants.SLOPE_HISPANIC)
		index_slope += index(slope(data[10], data[4]), the_constants.SLOPE_RENTERS) 

		#2. Education Scores
		X1_old = (data[16] + data[17]) / (data[14] + float(data[13]))
		X1_new = (data[22] + data[21]) / (data[19] + float(data[18]))
		index_pct += index(pct_change(X1_new, X1_old), the_constants.PCT_CHANGE_EDUCATION)
		index_slope += index(slope(X1_new, X1_old), the_constants.SLOPE_EDUCATION)

		#3. Occupation
		O1_old = data[24] / float(data[23])
		O1_new = data[28] / float(data[26])
		index_pct += index(pct_change(O1_new, O1_old), the_constants.PCT_CHANGE_EMPLOYMENT)
		index_slope += index(slope(O1_new, O1_old), the_constants.SLOPE_EMPLOYMENT)

		index_pct += index(pct_change(float(data[30]), data[25]), the_constants.PCT_CHANGE_PCI)
		index_slope += index(slope(float(data[30]), float(data[25])), the_constants.SLOPE_PCI)

		index_pct += index(pct_change(float(data[27]), data[31]), the_constants.PCT_CHANGE_INCOME)

		#4. Housing Built
		H1_old = sum([data[32], data[34], data[35]]) / float(data[32])
		H1_new = (data[36] + data[37]) / float(data[35])
		index_pct += index(pct_change(H1_new, H1_old), the_constants.PCT_CHANGE_HOUSING)
		index_slope += index(slope(H1_new, H1_old), the_constants.SLOPE_HOUSING)

		#5. Moving Score
		M1_old = (data[39] + data[40]) / float(data[38])
		M1_new = (data[42] + data[43]) / float(data[41])
		index_pct += index(pct_change(M1_new, M1_old), the_constants.PCT_CHANGE_MOVING)
		index_slope += index(slope(M1_new, M1_old), the_constants.SLOPE_MOVING)

		#6. Rent Score
		index_pct += index(pct_change(float(data[46]), float(data[44])), the_constants.PCT_CHANGE_RENT)
		index_slope += index(slope(float(data[46]), float(data[44])), the_constants.SLOPE_RENT)

		#Write the row
		return [name, index_pct, index_slope]


def special_write(writer, k, v):
	if k == "BNX":
		#write using BNX rules
		bnx_1_2 = get_combined_info(v[1], v[2])
		bnx_3_6 = get_combined_info(v[3], v[6])

		writer.writerow(special_results(bnx_1_2, k, "1&2"))
		writer.writerow(special_results(bnx_3_6, k, "3&6"))
		writer.writerow(special_results(v[4], k, "4"))
		writer.writerow(special_results(v[5], k, "5"))

		for j in range(7, num_of_cds[k] + 1):
			writer.writerow(special_results(v[j], k, str(j)))

	elif k == "MNH":
		#write using MNH rules
		bnx_1_2 = get_combined_info(v[1], v[2])
		bnx_4_5 = get_combined_info(v[4], v[5])

		writer.writerow(special_results(bnx_1_2, k, "1&2"))
		writer.writerow(special_results(bnx_4_5, k, "4&5"))
		writer.writerow(special_results(v[3], k, "3"))

		for j in range(6, num_of_cds[k] + 1):
			writer.writerow(special_results(v[j], k, str(j)))
	return 1

def gentrification_index(writer, k, v):
	if k == "BNX" or k == "MNH":
		return special_write(writer, k, v)

	borough = names_of_boroughs[k]

	for key in v:
		data = v[key]
		index_pct = 0
		index_slope = 0

		#1. Population Scores
		index_pct += -1 * index(pct_change(data[8]/float(data[6]), data[2]/float(data[0])), the_constants.PCT_CHANGE_BLACK)
		index_pct += index(pct_change(data[7]/float(data[6]), data[1]/float(data[0])), the_constants.PCT_CHANGE_WHITE)
		# index_pct += index(pct_change(data[9], data[3]), the_constants.PCT_CHANGE_HISPANIC)
		index_pct += index(pct_change(data[10], data[4]), the_constants.PCT_CHANGE_RENTERS)

		index_slope += index(slope(data[8], data[2]), the_constants.SLOPE_BLACK)
		index_slope += index(slope(data[7], data[1]), the_constants.SLOPE_WHITE)
		# index_slope += index(slope(data[9], data[3]), the_constants.SLOPE_HISPANIC)
		index_slope += index(slope(data[10], data[4]), the_constants.SLOPE_RENTERS) 

		#2. Education Scores
		X1_old = (data[16] + data[17]) / (data[14] + float(data[13]))
		X1_new = (data[22] + data[21]) / (data[19] + float(data[18]))
		index_pct += index(pct_change(X1_new, X1_old), the_constants.PCT_CHANGE_EDUCATION)
		index_slope += index(slope(X1_new, X1_old), the_constants.SLOPE_EDUCATION)

		#3. Occupation
		O1_old = data[24] / float(data[23])
		O1_new = data[28] / float(data[26])
		index_pct += index(pct_change(O1_new, O1_old), the_constants.PCT_CHANGE_EMPLOYMENT)
		index_slope += index(slope(O1_new, O1_old), the_constants.SLOPE_EMPLOYMENT)

		index_pct += index(pct_change(float(data[30]), data[25]), the_constants.PCT_CHANGE_PCI)
		index_slope += index(slope(float(data[30]), float(data[25])), the_constants.SLOPE_PCI)

		index_pct += index(pct_change(float(data[27]), data[31]), the_constants.PCT_CHANGE_INCOME)

		#4. Housing Built
		H1_old = sum([data[32], data[34], data[35]]) / float(data[32])
		H1_new = (data[36] + data[37]) / float(data[35])
		index_pct += index(pct_change(H1_new, H1_old), the_constants.PCT_CHANGE_HOUSING)
		index_slope += index(slope(H1_new, H1_old), the_constants.SLOPE_HOUSING)

		#5. Moving Score
		M1_old = (data[39] + data[40]) / float(data[38])
		M1_new = (data[42] + data[43]) / float(data[41])
		index_pct += index(pct_change(M1_new, M1_old), the_constants.PCT_CHANGE_MOVING)
		index_slope += index(slope(M1_new, M1_old), the_constants.SLOPE_MOVING)

		#6. Rent Score
		index_pct += index(pct_change(float(data[46]), float(data[44])), the_constants.PCT_CHANGE_RENT)
		index_slope += index(slope(float(data[46]), float(data[44])), the_constants.SLOPE_RENT)

		#Write the row
		writer.writerow([borough + " " + str(key), str(index_pct), str(index_slope)])

def main():
	# run main here
	init_dicts()

	#add the info from the csv files
	add_demographic_info(the_strings.DEMOGRAPHICS_OLD, the_strings.DEMOGRAPHICS_NEW)
	add_edu_info(the_strings.EDUCATION_OLD, the_strings.EDUCATION_NEW)
	add_occ_income_info(the_strings.OCCUPATION_OLD, the_strings.OCCUPATION_NEW)
	add_housing_info(the_strings.HOUSING_OLD, the_strings.HOUSING_NEW)
	add_moving_info(the_strings.MOVING_OLD, the_strings.MOVING_NEW)
	add_rent_info(the_strings.RENT_VALUE_OLD, the_strings.RENT_VALUE_NEW)

	write_csv()
	# write_population_csv()

main()