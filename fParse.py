#from bs4 import BeautifulSoup
#import requests
import os
import tmdbsimple as tmdb
import unicodedata
tmdb.API_KEY = '1975a12d6cafa9cccc4b7609ca785df0'

def makeMap():
	#open write file
	writeFile = open('map.txt', 'w')

	root = os.path.dirname(os.path.realpath(__file__))
	for root, dirs, files in os.walk(root):
		for file in files:
			file = os.path.join(root, file)
			if os.path.isfile(file):
				if file.endswith('.txt'):
					writers = []
					try:
						for writer in getAuthor(getTitle(file)):
							writers.append(writer)
							writers.append('#~ ')
						writeFile.write(getTitle(file) + '#~ ' + file + '#~ ' + (''.join(writers)) + '\n')
					except:
						pass
	#return

def titlify(title):
	result = title.replace(' ', '').replace('"', '').replace(':', '').replace(',','').replace('\'', '').replace('\n', '')
	result = result.lower()
	if result[:3] == 'the':
		result = result[4:] + 'the'
	return result
	
def getTitle(fileName):
	file = open(fileName, 'r')
	f = fileName.split('/')
	extName = f[len(f) - 1][0:-4]
	
	count = 0
	for line in file:
		if(count == 10):
			break
		for i in range(0, len(line)):
			for j in range(i + 1, len(line)):
				restring = line[i:j + 1]
				#print(restring + extName)
				if titlify(restring) == extName:
					#print('yay')
					return restring.replace('"', '').replace(',', '').strip()
		count += 1
	return 'titleNotFound'

def getAuthor(movieName):
	if movieName == 'titleNotFound':
		return ''
	search = tmdb.Search()
	search.movie(query = movieName)
	
	writers = []
	if(len(search.results) > 1):
		for c in tmdb.Movies(search.results[0]['id']).credits()['crew']:
			if c['job'] == 'Screenplay':
				for s in c['name'].split('\''): 
					if isinstance(s, str):
						writers.append(s)
					else:
						writers.append(unicodedata.normalize('NFKD', s).encode('ascii','ignore'))
		return writers
	else:
		return []
#print(getAuthor('Pulp Fiction'))
makeMap()