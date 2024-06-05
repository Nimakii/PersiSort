def exponential_search(x, A, start, cmp):
    '''Find position i >= start such that A[start:i] < x and A[i:] >= x.

    Comparisons A[i] < x are performed using cmp(A[i], x).
    '''
    low = start
    high = len(A)
    # Invariant: low <= i <= high
    # Exponential search
    d = 1
    while True:
        mid = start + d - 1
        if mid < high:
            if cmp(A[mid], x):
                low = mid + 1
                d *= 2
                continue
            high = mid
        break
    # Binary search
    while low < high:
        mid = (low + high) // 2
        if cmp(A[mid], x):
            low = mid + 1
        else:
            high = mid
    return low