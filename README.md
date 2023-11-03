# README #

A wrapper around mpi4py that offers simple scattering of iterable objects.

This is useful for embarassingly parallel, SPMD, type tasks that simply need to work on a list of things.

example usage:

`parfor_test.py`
```python
# import the parfor function; note
# that this will automatically initialize MPI
# also import pprint for parallel-friendly printing
from simplempi.parfor import parfor, pprint

# define a list to loop over
my_list = list(range(10)) 

# define a function that does something with each item in my_list
def func(i):
    return i**2

# loop in parallel over my_list
for i in parfor(my_list):
    result = func(i)
    pprint(f"{i}**2 = {result}")
```

Running this with mpirun on 4 processors shows that the list of 10 numbers gets
scattered as evenly as possible across all 4 processors; it also shows that the order of evaluation in the for loop is not well-defined (which is okay for embarassingly parallel code like this):

```bash
$ mpirun -n 4 python parfor_test.py 
(rank 1/4):  0**2 = 0
(rank 1/4):  4**2 = 16
(rank 1/4):  8**2 = 64
(rank 3/4):  2**2 = 4
(rank 3/4):  6**2 = 36
(rank 4/4):  3**2 = 9
(rank 4/4):  7**2 = 49
(rank 2/4):  1**2 = 1
(rank 2/4):  5**2 = 25
(rank 2/4):  9**2 = 81
```

Alternatively, one can use the object-oriented interface:

`simpleMPI_test.py`
```python
import simpleMPI

#Initialize MPI 
smpi = simpleMPI.simpleMPI()

#Make a list of things (20 numbers in this case)
testList = range(20)

#Scatter the list to all processors (myList differs among processes now)
myList = smpi.scatterList(testList)

#Print the list contents (as well as the rank of the printing process)
smpi.pprint(myList)
```

Running this with mpirun on 6 processors shows that the list of 20 numbers gets
scattered as evenly as possible across all 6 processors:

```bash
$ mpirun -n 6 python simpleMPI_test.py 
(rank 1/6): [0, 6, 12, 18]
(rank 2/6): [1, 7, 13, 19]
(rank 4/6): [3, 9, 15]
(rank 6/6): [5, 11, 17]
(rank 5/6): [4, 10, 16]
(rank 3/6): [2, 8, 14]

```