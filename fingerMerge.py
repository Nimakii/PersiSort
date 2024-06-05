from ExponentialSearch import exponential_search

def merge(A, B):
    '''Stable merging of two sorted lists.'''
    a = b = 0
    C = []
    while a < len(A) and b < len(B):
        if A[a] > B[b]:
            C.append(B[b])
            b += 1
        else:
            C.append(A[a])
            a += 1
    C.extend(A[a:])
    C.extend(B[b:])
    return C

def finger_merge(A, B):
    '''Merge two lists by alternating to perform exponential searches.'''

    # To get a stable sorting algorithm, the exponential searches
    # in A and B need to handle equality differently
    A_cmp = lambda x, y: x < y
    B_cmp = lambda x, y: not y < x  # x <= y
    a = b = 0
    C = []
    while a < len(A):
        b_ = exponential_search(A[a], B, b, A_cmp)
        C.extend(B[b:b_]) #b_ - b   
        C.append(A[a])
        b = b_
        a += 1
        # swap A and B
        a, A, A_cmp, b, B, B_cmp = b, B, B_cmp, a, A, A_cmp  
    C.extend(B[b:])
    return C

def finger_merge_22(A,B,C):
    if not A:
        return finger_merge(B,C)
    if not B:
        return finger_merge(A,C)
    if not C:
        return finger_merge(A,B)
    return finger_merge(A,finger_merge(C,B))
    if not A:
        return finger_merge(B,C)
    if not B:
        return finger_merge(A,C)
    if not C:
        return finger_merge(A,B)
    a = b = c = 0
    D = []
    # To get a stable sorting algorithm, the exponential searches
    # in A and B need to handle equality differently
    cmp = lambda x, y: x < y
    while a < len(A):
        b_ = exponential_search(A[a], B, b, cmp)
        c_ = exponential_search(A[a], C, c, cmp)
        D.extend(finger_merge(B[b:b_],C[c:c_]))
        D.append(A[a])
        b = b_
        c = c_
        a += 1
        
        if a == len(A):
            return D + finger_merge(B[b:],C[c:])
        elif b == len(B):
            return D + finger_merge(A[a:],C[c:])
        elif c == len(C):
            return D + finger_merge(B[b:],C[c:])

        if A[a] <= B[b] and A[a] <= C[c]:
            pass
        elif B[b] <= A[a] and B[b] <= C[c]:
            # swap A,B,C to B,C,A
            A,a,B,b,C,c = B,b,C,c,A,a
        else: # C[c] <= A[a] and C[c] <= B[b]
            # swap A,B,C to C,A,B
            A,a,B,b,C,c = C,c,A,a,B,b
    #Unreachable
    print("unreachable")
    C.extend(B[b:])
    return C

if __name__ == "__main__":
    pass