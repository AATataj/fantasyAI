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

def testList ():
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
    LastNode=None
    for i in range(5,0,-1):
        newNode = ListNode(i, LastNode)
        LastNode = newNode
        if i == 1 :
            head = newNode
    currentNode=head
    while(1):
        print(currentNode.val)
        if currentNode.next!=None:
            currentNode=currentNode.next
        else:
            break
    currentNode = removeNthLast(head, 4)
    print ("results")
    while(1):
        print(currentNode.val)
        if currentNode.next!=None:
            currentNode=currentNode.next
        else:
            break
    return

def removeNthLast(head, n):
    if head == None:
        return None
    if head.next==None and n==1:
        return None
    currentNum = 1
    currentNode = head
    prevNode = None
    while (1):
        currentNum+=1
        # when we get to n elements into list
        # assign/increment prevNode
        if currentNum == (n+1):
            prevNode=head
        elif currentNum > (n+1):
            prevNode=prevNode.next
        # increment currentNode afterwards
        currentNode=currentNode.next
        # if end of list
        if currentNode.next==None:
            # if end of list reached at the n'th element
            if currentNum == n:
                #reassign head
                head = head.next
                #prevNode.next=None
                break
            else:
                # otherwise, cur out the n'th element
                prevNode.next=prevNode.next.next
                break
    
    return head

def searchMatrix(matrix, target):
        row = 0
        if matrix == [] or matrix[0]==[]:
            return False
        if target > matrix[len(matrix)-1][len(matrix[0])-1]:
            return False
        for i in range(len(matrix)):
            if target == matrix[i][0]:
                return True
            if i+1 < len(matrix) and target > matrix[i][0] and target < matrix[i+1][0]:
                row = i
                break
            elif i+1 == len(matrix) :
                row = len(matrix) - 1
                break
        for i in range (len(matrix[row])):
            if target == matrix[row][i]:
                return True
        
        return False

## validate BST 
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        leftSubTree = rightSubTree = True
        if root == None : 
            return True
        if root.right == None and root.left == None:
            return True
        if root.left is not None:
            if root.left.val > root.val:
                return False
            else :
                leftSubTree = Solution.isValidBST(self, root.left) and (Solution.maxSub(self, root.left) < root.val)
        if root.right is not None:
            if root.right.val < root.val :
                return False
            else :
                rightSubTree = Solution.isValidBST(self, root.right) and (Solution.minSub(self, root.right) > root.val)
        if rightSubTree and leftSubTree:
            return True
        else :
            return False
    def maxSub(self, root : TreeNode) -> int:
        node = root
        if node.right == None:
            return node.val
        while(1):
            if node.right == None:
                return node.val
            else:
                node = node.right
    def minSub(self, root : TreeNode) -> int:
        node = root
        if node.left == None:
            return node.val
        while(1):
            if node.left == None:
                return node.val
            else:
                node = node.left

## Delete node in BST
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        # base case
        if root == None:
            return None
        #traverse until found
        if key > root.val and root.right is not None:
            root.right = Solution.deleteNode(self, root.right, key)
        elif key < root.val and root.left is not None:
            root.left = Solution.deleteNode(self, root.left, key)
        # if found, return the right or left chile if one child
        # elif return min of greater side as the root
        # else leaf node, return none  
        elif root.val == key:
            if root.right is not None and root.left is None :
                return root.right
            elif root.left is not None and root.right is None:
                return root.left
            elif root.left is not None and root.right is not None:
                minNode = Solution.minSub(self, root.right)
                minNode.right = Solution.deleteNode(self, root.right, minNode.val)
                minNode.left = root.left
                return minNode
            else :
                return None
        return root
    def minSub(self, root : TreeNode) -> TreeNode:
        node = root
        if node.left == None:
            return node
        while(1):
            if node.left == None:
                return node
            else:
                node = node.left        