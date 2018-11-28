def mapReader(fileName):
	file = open(fileName, 'r')
	map = {}
	for line in file:
		f = line.strip().split('#~ ')
		map[f[0]] = f[1:]
	return map

print(mapReader('map.txt'))