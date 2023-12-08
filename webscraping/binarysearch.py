def BinarySearch(arr, x):
    ''' returns location of x in given array arr '''
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
