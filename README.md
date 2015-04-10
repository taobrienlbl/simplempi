# README #

A simple wrapper around mpi4py that offers simple scattering of a list of objects.

This is useful for embarassingly parallel, SPMD, type tasks that simply need to work on a list of things.

example usage:

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
