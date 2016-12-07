import csv
import numpy as np


def read_csv():
    nhl_data = list()
    with open('data.csv', 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        next(r, None)
        for data in r:
            nhl_data.append(data[4:])

    matrix = np.array(nhl_data).astype(np.float)
    print(len(matrix))

    cor_matrix = np.corrcoef(matrix.T)

    return cor_matrix

def determine_correlation(data):

    # round all numbers in the correlation matrix to the
    # nearest 5 decimal places.
    correlation_data = list()
    rounded_list = [['%.5f' % round(y, 5) for y in x] for x in data]
    for x in rounded_list:
        print(x)


def main():
    data = read_csv()
    determine_correlation(data)


if __name__ == '__main__':
    main()
