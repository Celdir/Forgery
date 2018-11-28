def mapReader(fileName):
	file = open(fileName, 'r')
	map = {}
	for line in file:
		f = line.split('#~ ')
                f = [s.strip() for s in f]
		map[f[0]] = f[1:]
	return map

print(mapReader('map50.txt'))
