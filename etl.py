import re
import numpy as np
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm

x = []
y = []


def get_len(url):
    return len(url)

def get_url_count(url):
    if re.search('(http://)|(https://)', url, re.IGNORECASE) :
        return 1
    else:
        return 0

def get_evil_char(url):
    return len(re.findall("[<>,\'\"]", url, re.IGNORECASE))

def get_evil_word(url):
    return len(re.findall("(alert)|(script)|(%3c)|(%3e)|(%20)|(onerror)|(onload)|(eval)|(src=)|(prompt)",url,re.IGNORECASE))



def etl(filename,data,isxss):
    try:
        file_object = open(filename)
        for line in file_object:
            f1=get_len(line)
            f2=get_url_count(line)
            f3=get_evil_char(line)
            f4=get_evil_word(line)
            data.append([f1,f2,f3,f4])
            if isxss:
                y.append(1)
            else:
                y.append(0)
    finally:
        file_object.close( )
    return data

etl('xss-10000.txt',x,1)
etl('good-xss-10000.txt',x,0)


x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y, test_size=0.4, random_state=0)

clf = svm.SVC(kernel='linear', C=1).fit(x_train, y_train)
print clf.score(x_test, y_test)

