import elementtree.ElementTree as ET
import sys
import hashlib

# load command line argument (xml file name)
xmlfile = sys.argv[1]

# load the object that will hash things


# parse the xml file
crimeTree = ET.parse(xmlfile)

# regular expression to use for each json field
jsonField = '\"%s\" : \"%s\" %s\n'

# flag indicating first entry
firstEntry = True

# fields to store the lattitude and longitude
lat = 0.0;
long = 0.0;

#last field of the entry to know when to finish the json entry
lastField = 'LonY'

commaChar = ','

# loop through each crime data node
for crimeNode in crimeTree.findall('class'):

		
		#now get the inner node
		# print crimeNode.attrib['name'] ,':', ' serg'
		
		# all the crime info
		crimeData = list(crimeNode.getiterator())
		
		# loop through every child in the xml. deep traversal
		for crimeElement in crimeData:
			
			#if first entry, just print out initial opening brackets
			if firstEntry:
				print '['
				print '{'
				firstEntry = False
				continue
			
			# if we encounter a class tag
			if crimeElement.tag == 'class':
				
				# we are in a new crime entry, start new json entry
				if crimeElement.attrib['name'] == 'ciras.db.Crime':
					print '},'
					print '{'
				
				#else, its probably an address or something else
				continue

			# if not the last field, comma will be added an end of this field
			if crimeElement.attrib['name'] != lastField:
				commaChar = ','
			else:
				commaChar = ''
			
			
			# create the id hash from the crimeNumber
			if crimeElement.attrib['name'] == 'CrimeNumber':
				sys.stdout.write(jsonField % ('id', hashlib.md5(crimeElement.text).hexdigest(), commaChar))
			# ignore SRID
			elif crimeElement.attrib['name'] == 'SRID':
				continue
			# create a date from the File field
			elif crimeElement.attrib['name'] == 'File':
				date = crimeElement.text.replace('.txt','').split('-')
				solrDateFormat = date[2]+'-'+date[0]+'-'+date[1]+"T23:59:59Z"
				sys.stdout.write(jsonField % ('crimeDate', solrDateFormat, commaChar))
			# Lattitude, store it
			elif crimeElement.attrib['name'] == 'LatX':
				lat = crimeElement.text
			# longitude. means we have both Geo fields an we can add it as a field
			elif crimeElement.attrib['name'] == 'LonY':
				lon = crimeElement.text
				sys.stdout.write(jsonField % ('coordinates',  lat+','+lon, commaChar))
			# normal field add it
			else: 
				sys.stdout.write(jsonField % (crimeElement.attrib['name'].lower(),  crimeElement.text, commaChar))
				
			# print crimeElement.tag
print '}'
print ']'

