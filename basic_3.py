import sys
import time
import psutil

string1=''
string2=''

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def optimalStringCheck():
    string1, string2 = readInput()
    optimalSoln = [[0 for m in range(len(string2)+1)] for n in range(len(string1)+1)]

    delta = 30

    alpha = [[0, 110, 48, 94],
             [110, 0, 118, 48],
             [48, 118, 0, 110],
             [94, 48, 110, 0]]

    alpha_mapping={
        'A' : 0,
        'C' : 1,
        'G' : 2,
        'T' : 3
    }

    #initialize
    for m in range(0, len(string1)+1):
        optimalSoln[m][0]=m*delta
    for n in range(0, len(string2)+1):
        optimalSoln[0][n]=n*delta
    for m in range(0, len(string1)):
        for n in range(0, len(string2)):
            optimalSoln[m+1][n+1] = min(alpha[alpha_mapping[string1[m]]][alpha_mapping[string2[n]]]+optimalSoln[m][n],
                                            delta+optimalSoln[m][n+1],
                                            delta+optimalSoln[m+1][n])


    return {
        'optimalSoln' : optimalSoln,
        'delta' : delta,
        'alpha' : alpha,
        'alpha_mapping' : alpha_mapping,
        'string1' : string1,
        'string2' : string2
    }

def backTrack():
    backPropString1 = ''
    backPropString2 = ''
    optimalSolnOutput = optimalStringCheck()
    optimalSoln = optimalSolnOutput['optimalSoln']
    alphaValues = optimalSolnOutput['alpha']
    alphaMapping = optimalSolnOutput['alpha_mapping']
    string1 = optimalSolnOutput['string1']
    string2 = optimalSolnOutput['string2']

    m = len(optimalSolnOutput['string1'])
    n = len(optimalSolnOutput['string2'])

    cost = optimalSoln[m][n]
    optValue = optimalSoln[m][n]
    while(m>0 and n>0):
        b1 = optimalSoln[m-1][n] + optimalSolnOutput['delta']
        b2 = optimalSoln[m][n-1]+ optimalSolnOutput['delta']
        b3 = optimalSoln[m-1][n-1]+ alphaValues[alphaMapping[string1[m-1]]][alphaMapping[string2[n-1]]]

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

    backPropString1 = backPropString1[::-1]
    backPropString2 = backPropString2[::-1]

    return backPropString1, backPropString2, cost

def checkInteger(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def printOutput(filename):
    f = open(filename, "w")
    start_time = time.time()

    backTrackedData = backTrack()
    f.write(str(backTrackedData[2])+ '\n')
    f.write(backTrackedData[0]+ '\n')
    f.write(backTrackedData[1]+ '\n')

    f.write(str((time.time() - start_time)*1000)+ '\n')
    f.write(str(process_memory())+ '\n')
    f.close()

def readInput():
    inputfilename = sys.argv[1]
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

if __name__== '__main__':
    outfilename = sys.argv[2]
    printOutput(outfilename)
