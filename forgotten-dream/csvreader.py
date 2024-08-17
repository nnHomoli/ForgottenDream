from csv import reader

def Read_Map_CSV(csvLocation):
    csvMap = []
    with open(csvLocation, 'r') as csvFile:
        csvReader = reader(csvFile, delimiter=',')
        for row in csvReader:
            csvMap.append(list(row))
        return csvMap