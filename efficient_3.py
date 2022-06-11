import sys
from resource import *
import time
import psutil
import math
import os

def readInput(inputfilename):
    with open(inputfilename, 'r') as f:
        flag=0
        string1 = ''
        string2 = ''
        for lines in f.readlines():
            lines = lines.rstrip()
            if(not checkInteger(lines)):
                flag+=1
                if flag ==1:
                    string1 = string1 + lines
                else:
                    string2= string2 + lines
            else:
                lines = int(lines)
                if flag == 1:
                    string1 = string1[:lines+1] + string1 + string1[lines+1:]
                else:
                    string2 = string2[:lines+1] + string2 + string2[lines + 1:]

        return string1, string2

def optimalStringCheck_complete(string1, string2):
    optimalSoln = [[0 for m in range(len(string2) + 1)] for n in range(len(string1) + 1)]

    delta = 30
    alpha = [[0, 110, 48, 94],
             [110, 0, 118, 48],
             [48, 118, 0, 110],
             [94, 48, 110, 0]]
    alpha_mapping = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3
    }

    # initialization
    for m in range(0, len(string1)+1):
        optimalSoln[m][0] = m * delta
    for n in range(0, len(string2)+1):
        optimalSoln[0][n] = n * delta
    for m in range(0, len(string1)):
        for n in range(0, len(string2)):
            optimalSoln[m + 1][n + 1] = min(
                alpha[alpha_mapping[string1[m]]][alpha_mapping[string2[n]]] + optimalSoln[m][n],
                delta + optimalSoln[m][n + 1],
                delta + optimalSoln[m + 1][n])

    cost = optimalSoln[len(string1)][len(string2)]
    align1, align2 = backTrack(optimalSoln, string1, string2)
    return align1, align2, cost

def backTrack(optimalSoln, string1, string2):
    backPropString1 = ''
    backPropString2 = ''

    delta = 30
    alpha = [[0, 110, 48, 94],
             [110, 0, 118, 48],
             [48, 118, 0, 110],
             [94, 48, 110, 0]]

    alpha_mapping = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3
    }
    m = len(string1)
    n = len(string2)
    while(m>0 and n>0):
        optValue = optimalSoln[m][n]
        b1 = optimalSoln[m-1][n] + delta
        b2 = optimalSoln[m][n-1]+ delta
        b3 = optimalSoln[m-1][n-1]+ alpha[alpha_mapping[string1[m-1]]][alpha_mapping[string2[n-1]]]

        if (optValue == b3):
            backPropString1 = backPropString1+string1[m-1]
            backPropString2 = backPropString2+string2[n-1]
            optValue = optimalSoln[m-1][n-1]
            m=m-1
            n=n-1

        elif(optValue == b2):
            backPropString1 = backPropString1+'_'
            backPropString2 = backPropString2 + string2[n-1]
            optValue = optimalSoln[m][n - 1]
            n = n-1

        elif(optValue == b1):
            backPropString1 = backPropString1 + string1[m-1]
            backPropString2 = backPropString2 + '_'
            optValue = optimalSoln[m - 1][n]
            m = m-1

    while(n>0):
        backPropString1 = backPropString1 + '_'
        backPropString2 = backPropString2 + string2[n-1]
        optValue = optimalSoln[m][n-1]
        n=n-1

    while(m>0):
        backPropString1 = backPropString1 + string1[m-1]
        backPropString2 = backPropString2 + '_'
        optValue = optimalSoln[m-1][n]
        m=m-1

    return backPropString1, backPropString2

def divideString(string1, string2):

    if len(string1) <= 1 or len(string2) <= 1:
        align1, align2, cost = optimalStringCheck_complete(string1, string2)
        return align1, align2, cost

    string1_left = string1[0:math.floor(len(string1)/2)]
    string1_right = string1[math.floor(len(string1)/2): len(string1)]

    left=optimalStringCheck(string1_left,string2)
    right=optimalStringCheck(string1_right[::-1],string2[::-1])

    concat_array = []
    for i in range(len(left)):
        concat_array.append(left[i] + right[len(left)-i-1])

    min_cost = concat_array[0]
    min_index = 0
    for i in range(len(left)):
        if min_cost > concat_array[i]:
            min_cost = concat_array[i]
            min_index = i

    if (min_index == 0 or min_index == len(string2)):
        cost, align1, align2 = optimalStringCheck_complete(string1, string2)
        return cost, align1, align2

    c1, output_l1, output_l2 = divideString(string1_left, string2[0:min_index])
    c2, output_r1, output_r2 = divideString(string1_right, string2[min_index:len(string2)])
    return c1+c2, output_l1+output_r1, output_l2+output_r2

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def optimalStringCheck(string1, string2):
    optimalSoln = [[0 for m in range(len(string2)+1)] for n in range(2)]
    delta = 30

    alpha = [[0, 110, 48, 94],
             [110, 0, 118, 48],
             [48, 118, 0, 110],
             [94, 48, 110, 0]]

    alpha_mapping={
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3
    }

    for n in range(0, len(string2)+1):
        optimalSoln[0][n]=n*delta

    for m in range(0, len(string1)):
        optimalSoln[1][0]= (m+1)*delta
        for n in range(0, len(string2)):
            optimalSoln[1][n+1] = min(alpha[alpha_mapping[string1[m]]][alpha_mapping[string2[n]]]+optimalSoln[0][n],
                                            delta+optimalSoln[0][n+1],
                                            delta+optimalSoln[1][n])

        for n in range(0, len(string2)+1):
            optimalSoln[0][n] = optimalSoln[1][n]


    return optimalSoln[1]

def checkInteger(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def printOutput(output1, output2, cost, time_taken, memory):
    output = sys.argv[2]
    if os.path.exists(output):
        os.remove(output)
    with open(output, 'a') as f:
        f.write(str(cost) + '\n')
        f.write(str(output1) + '\n')
        f.write(str(output2) + '\n')
        f.write(str(time_taken) + '\n')
        f.write(str(process_memory())+ '\n')

def getFileDatas():
    inputFile = sys.argv[1]
    inputs = readInput(inputFile)
    return inputs

if __name__== '__main__':
    start_time = time.time()
    getFileDatas = getFileDatas()
    start_time = time.time()
    output1, output2, cost = divideString(getFileDatas[0], getFileDatas[1])
    memory_taken = process_memory()
    printOutput(output1, output2, cost ,((time.time() - start_time)* 1000), memory_taken)