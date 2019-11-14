import csv
def r_csv(x,mode='rt', delim = ','):
    l = []
    csv_in = open(x, mode, encoding = 'utf-8')
    myreader = csv.reader(csv_in, delimiter = delim)
    for row in myreader:
        l.append(row)
    csv_in.close()
    return l