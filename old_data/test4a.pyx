def compute(int loop_a, int loop_b):
    cdef int result = 0

    for a in range(loop_a):
        for b in range(loop_b):
            result += 1
    return result