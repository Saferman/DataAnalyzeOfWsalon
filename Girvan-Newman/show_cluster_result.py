# encoding:utf8
import pickle
# 使用task_one_D.pickle跑到的结果
# result_salon_without_tag = [set([1]), set([2]), set([3]), set([4]), set([5]), set([6]), set([48, 9, 19, 49, 7]), set([8,10,11]), set([50, 12, 13, 45]), set([42, 22, 14]), set([32, 37, 46, 15, 26, 30]), set([16]), set([17]), set([18]), set([20]), set([21]), set([23]), set([24]), set([25]), set([27]), set([28]), set([29]), set([31]), set([33]), set([34, 51]), set([35]), set([36]), set([38]), set([39]), set([40]), set([41]), set([43]), set([44]), set([47])]
# result = [set([1]), set([2, 4, 53, 14]), set([3, 39]), set([43, 5]), set([6]), set([7, 8, 45, 48, 40, 18, 28]), set([9]), set([32, 10, 51]), set([11]), set([12]), set([13]), set([15]), set([16]), set([17, 50, 41]), set([19]), set([20]), set([21]), set([22]), set([38, 23]), set([24]), set([25]), set([26]), set([44, 27, 52, 30]), set([29]), set([31]), set([33]), set([34]), set([35]), set([36]), set([37]), set([42]), set([46]), set([47]), set([49])]
# 使用task_one_MG.pickle跑到的结果
# 下面这个result没有具体固定含义
result =  [set([1]), set([2, 36, 6, 9, 18, 41]), set([3]), set([4]), set([5]), set([7]), set([8]), set([10]), set([11]), set([20, 43, 12, 21]), set([13]), set([14]), set([15]), set([16]), set([17]), set([19]), set([22]), set([23]), set([24]), set([25]), set([26]), set([27]), set([28]), set([29]), set([30]), set([31]), set([32]), set([33]), set([34]), set([35]), set([37]), set([38]), set([39]), set([40]), set([42]), set([44])]


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

