import pdb
## given a list and a target, find len=2 lists which sum to target
# nums = [2,7,11,15]
# target = 9

# map = {}
# pdb.set_trace()
# for i in range(len(nums)):
#     needed = target - nums[i]
#     if needed in map:
#         print(str([map[needed], i]))
#     map[needed] = i

# print ("end")

# outstr=""
# string = str(x)
# for c in range(len(string)):
#     print (string[len(string)- 1 - c])
#     outstr+=string[len(string)- 1 - c]
#     print(outstr)

# print(outstr)
# 

## reverse order of int without casting to string aka find if int is a palendrome
# x=15321
# out=0
# if x < 0:
#     print(False)
# else:
#     reversed = 0
#     current = x
#     while(1):
#         #pdb.set_trace()
#         out = int(out*10+(current%10))
#         current = int(current - (current%10))/10
#         print (str(out))
#         if current==0:
#             break

# if out == x :
#     print(True)
# else:
#     print(False)    
    

## verify legal bracketting syntax
# string = "(){}}{"
# print(string)
# if string == "":
#     print (False)
# if len(string)%2 !=0 or string[0] == "}" or string[0] == ")" or string[0] == "]" :
#     print(False)

# substring = ""

# for char in range(len(string)):
#     #pdb.set_trace()
#     if string[char] == "(":
#         substring+="("
#     elif string[char] == "{":
#         substring+="{"
#     elif string[char] == "[":
#         substring+="["
#     elif string[char] == ")" and substring[len(substring)-1] == "(":
#         substring =substring[:-1]
#     elif string[char] == "}" and substring[len(substring)-1] == "{":
#         substring =substring[:-1]
#     elif string[char] == "]" and substring[len(substring)-1] == "[":
#         substring =substring[:-1]
#     else :
#         print(False)
#         break
# if len(substring) == 0:
#     print(True)
# else :
#     print(False)

## merge two sorted lists
# l1 = [1,2,4]
# l2 = [1,3,4]
# if l1 ==[]  and l2 == []:
#     return []
# if l1 == []:
#     return l2
# if l2 == []
#     return l1
# out =[]
# l2remain = l2
# for elem1 in l1:
#     for elem2 in l2remain:
#         if elem1 < elem2:
#             out.append(elem1)
#             break
#         else :
#             out.append(elem2)
#             l2remain = l2remain[1:]

# print(out)

## mergesort complexity = nlog(n)
def mergeSorrt(arr): 
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        mergeSorrt(L)
        mergeSorrt(R)
        i=j=x=0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[x]=L[i]
                i+=1
            else :
                arr[x]=R[j]
                j+=1
            x+=1
        if i < len(L):
            for i in range(i, len(L)):
                arr[x]=L[i]
                x+=1
        if j < len(R):
            for j in range(j, len(R)):
                arr[x]=R[j]
                x+=1 

        print("left : " + str(L) + " right : " + str(R) + " result : " + str(arr))
        return  arr
    
# lists are 'mutable' meaning you change a parameter locally in the function, it alters the global version
# integers are not, you modify the value in a function, the global value doesn't change
# due to pointers in the underlying c code?
def test (x):
    temp=x[0]
    x[0] = x[1]
    x[1] = temp
    return x
def test2(y):
    y=y+1
    return y

# bubble sort complexity = n^2
def bubbleSort(arr):
    swap = False
    while (1):
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                temp = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = temp
                swap=True
        if not swap:
            break
        swap=False
    return arr

# insertion sort complexity n^2
def insertionSort(arr):
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[i]< arr[j]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j]=temp
    return arr

# quicksort complexity worst : n^2, avg : nlogn
def quickSort(arr, lowIndex, hiIndex):
    #pdb.set_trace()
    if lowIndex < hiIndex:
        partitionIndex = partition(arr, lowIndex, hiIndex)
        quickSort(arr, lowIndex, partitionIndex-1)
        quickSort(arr, partitionIndex+1, hiIndex)
def partition(arr, lowIndex, hiIndex):
    # set the partition value to last element
    partitionValue = arr[hiIndex]
    # j is used as a an index for the number of elements less than the partition value
    j=lowIndex
    # loop from low bound to high
    for i in range(lowIndex, hiIndex):
        # if the current array value is less than the partition value
        if arr[i] < partitionValue:
            # swap
            temp = arr[j]
            arr[j] = arr[i]
            arr[i] = temp
            # increment the number of elements less than the partition value
            j+=1
            print(arr)
    print(arr)
    # swap the partition element to it's correct position using the counter 
    temp=arr[j]
    arr[j]=arr[hiIndex]
    arr[hiIndex]=temp
    # return that partition value for recursive calls
    return j

# remove matching nodes from singly linked list
def removeFromList(l, t):
    if l == None:
        return None
    currentNode = l
    while (currentNode != None):
        if currentNode.value == t and currentNode != l:
            lastNode.next = currentNode.next
        else:
            lastNode = currentNode
        currentNode = currentNode.next
    if l.value == t:
        return l.next
    else :
        return l

# power set of a set that contains no duplicates in the power set:

def powerSet (inset):
    setItems = {}
    powerset = []
    for i in range(len(inset)):
        if inset[i] in setItems:
            setItems[inset[i]]+=1
        else:
            setItems[inset[i]]=1
    for item in setItems:
        addSet = []
        for numitems in range(setItems[item]):
            addSet.append[item]
            #powerset.append(str(item)*(numitems+1))
            powerset.append(addSet)
    print(powerset)
    powerset=computePower(powerset)
    #powerset.append([])        
def lenLongestSubstr(string):
    if string == "":
        return 0
    length = 0
    max = 0
    seen = {}
    print (string)
    for index in range(len(string)):
        #pdb.set_trace()
        if string[index] not in seen:
            length+=1
            seen[string[index]] = index    
        else :
            if length >= index-seen[string[index]]:
                length= index-seen[string[index]]
            else:
                length+=1
                print(str(length)+ " " + str(string[index]) + " " + str(index))
            seen[string[index]]=index
        if length > max:
            max = length
    return max