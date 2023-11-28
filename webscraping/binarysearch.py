# Python3 code to implement iterative Binary
# Search.
 
 
# It returns location of x in given array arr
def BinarySearch(arr, x):
    l = 0
    r = len(arr)-1
 
    while l <= r:
        mid = l + (r - l) // 2
 
        if arr[mid] == x:
            return mid
 
        elif arr[mid] < x:
            l = mid + 1
 
        else:
            r = mid - 1
 
    return -1
 
 
# Driver Code
if __name__ == '__main__':
    arr = [2, 3, 4, 10, 40]
    x = 10
 
    # Function call
    result = BinarySearch(arr, 5)
    if result != -1:
        print("Element is present at index", result)
    else:
        print("Element is not present in array")