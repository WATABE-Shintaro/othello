import time
import test4 as cs
import test4a as csa
import test3 as ps
import test4b as csb

start = time.time()
result = csb.compute(10000,10000)

end = time.time()
print(result)
print("The time takes is {}".format(end-start))

start = time.time()
result = csa.compute(10000,10000)

end = time.time()
print(result)
print("The time takes is {}".format(end-start))

start = time.time()
result = cs.compute(10000,10000)

end = time.time()
print(result)
print("The time takes is {}".format(end-start))

start = time.time()
result = ps.compute(10000,10000)

end = time.time()
print(result)
print("The time takes is {}".format(end-start))