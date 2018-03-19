# encoding:utf8
import pickle
result = [set([1]), set([2]), set([3]), set([4]), set([5]), set([6]), set([48, 9, 19, 49, 7]), set([8,10,11]), set([50, 12, 13, 45]), set([42, 22, 14]), set([32, 37, 46, 15, 26, 30]), set([16]), set([17]), set([18]), set([20]), set([21]), set([23]), set([24]), set([25]), set([27]), set([28]), set([29]), set([31]), set([33]), set([34, 51]), set([35]), set([36]), set([38]), set([39]), set([40]), set([41]), set([43]), set([44]), set([47])]


def show():
    f = open("remapped.pickle",'r')
    remapped = pickle.load(f)
    f.close()

    for item in result:
        for item2 in item:
            print remapped[item2]+",",
        print "\n",

if __name__ == '__main__':
    show()

