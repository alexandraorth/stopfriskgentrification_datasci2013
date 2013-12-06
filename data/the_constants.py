# Khalid Richards
# the_constants.py

# Population
PCT_CHANGE_WHITE = ((2722904.0 / 8175133) - (2801267.0 / 8008278.0)) / (2801267.0 / 8008278.0)
PCT_CHANGE_BLACK = ((1861295.0 / 8175133) - (1962154.0 / 8008278.0)) / (1962145.0 / 8008278.0)
PCT_CHANGE_HISPANIC = ((2336076.0 / 8175133) - (2160554.0 / 8008278.0)) / (2160554.0 / 8008278.0)

SLOPE_WHITE = ((2722904.0 / 8175133) - (2801267.0 / 8008278.0)) / 10.0
SLOPE_BLACK = ((1861295.0 / 8175133) - (1962154.0 / 8008278.0)) / 10.0
SLOPE_HISPANIC = ((2336076.0 / 8175133) - (2160554.0 / 8008278.0)) / 10.0

# Renting
PCT_CHANGE_RENTING = ((2071279.0 / 3046695.0) - (2109292.0 / 3021588)) / (2109292.0 / 3021588)
SLOPE_RENTING = ((2071279.0 / 3046695.0) - (2109292.0 / 3021588)) / 10.0

# Education
X1_2000 = (632595 + 830095) / 5276946.0
X2_2000 = (1446833 + 834558) / 5276946.0
X3_2000 = X2_2000 / X1_2000

X1_2010 = (593733 + 551245) / 5557330.0
X2_2010 = (1107924 + 766412) / 5557330.0
X3_2010 = X2_2010 / X1_2010

PCT_CHANGE_EDUCATION = X3_2010 - X3_2000 / X3_2000
SLOPE_EDUCATION = (X3_2010 - X3_2000) / 10

# Employment
M1_2000 = 1206052 / 3277825.0
M1_2010 = 1408410 / 3722698.0
PCT_CHANGE_EMPLOYMENT = (M1_2010 - M1_2000) / M1_2000
SLOPE_EMPLOYMENT = (M1_2010 - M1_2000) / 10

# Median Income
PCT_CHANGE_INCOME = (50331.0 - 38293.0) / 38293.0
SLOPE_INCOME = (50331.0 - 38293.0) / 10

# Per Capita Income
PCT_CHANGE_PCI = (30717 - 22402) / 22402.0
SLOPE_PCI = (30717.0 - 22402.0) / 22402.0

# Housing
H1_2000 = (19774.0 + 51061.0 + 61106.0) / 3200912.0
H1_2010 = (104909.0 + 98945.0) / 3370989.0
PCT_CHANGE_HOUSING = (H1_2010 - H1_2000) / H1_2000
SLOPE_HOUSING = (H1_2010 - H1_2000) / 10.0

# Moving
V1_2000 = (443358.0 + 859136.0) / 3021588.0
V2_2010 = 1257430.0 / 3046695.0
PCT_CHANGE_MOVING = (V2_2010 - V1_2000) / V1_2000
SLOPE_MOVING = (V2_2010 - V2_2010) / 10.0

# Median Renting
PCT_CHANGE_RENT = (1152.0 - 705.0) / 705.0
SLOPE_RENT = (1152.0 - 705.0) / 10.0

# Median Housing Value
PCT_CHANGE_MHV = (502100.0 - 211900.0) / 211900.0
SLOPE_MHV = (502100.0 - 211900.0) / 10.0