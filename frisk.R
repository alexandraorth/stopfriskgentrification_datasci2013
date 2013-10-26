library(sqldf)

# read in csvs
# d2005 <- read.csv("data/2005_frisk.csv")
# d2006 <- read.csv("data/2006_frisk.csv")
# d2007 <- read.csv("data/2007_frisk.csv")
# d2008 <- read.csv("data/2008_frisk.csv")
# d2009 <- read.csv("data/2009_frisk.csv")
# d2010 <- read.csv("data/2010_frisk.csv")
# d2011 <- read.csv("data/2011_frisk.csv")


# data for total number of stops in each district
total_data <- sqldf("SELECT year, addrpct, count(addrpct) FROM d2005 WHERE addrpct IN (79, 83, 77, 71, 84, 76) GROUP BY addrpct
	UNION ALL 
	SELECT year, adrpct, count(adrpct) FROM d2006 WHERE adrpct IN (79, 83, 77, 71, 84, 76) GROUP BY adrpct
	UNION ALL
	SELECT year, addrpct, count(addrpct) FROM d2007 WHERE addrpct IN (79, 83, 77, 71, 84, 76) GROUP BY addrpct
	UNION ALL
	SELECT year, addrpct, count(addrpct) FROM d2008 WHERE addrpct IN (79, 83, 77, 71, 84, 76) GROUP BY addrpct
	UNION ALL
	SELECT year, addrpct, count(addrpct) FROM d2009 WHERE addrpct IN (79, 83, 77, 71, 84, 76) GROUP BY addrpct
	UNION ALL
	SELECT year, addrpct, count(addrpct) FROM d2010 WHERE addrpct IN (79, 83, 77, 71, 84, 76) GROUP BY addrpct
	UNION ALL
	SELECT year, addrpct, count(addrpct) FROM d2011 WHERE addrpct IN (79, 83, 77, 71, 84, 76) GROUP BY addrpct")

