""" Automatically initialize MPI on import for simple use of parallel loops. 

Example usage:

```python
# import the parfor function; note
# that this will automatically initialize MPI
from simplempi.parfor import parfor

# define a list to loop over
my_list = list(range(10)) 

# define a function that does something with each item in my_list
def func(i):
    return i**2

# loop in parallel over my_list
for item in parfor(my_list):
    func(item)
"""
import simplempi

# Initialize MPI
smpi = simplempi.simpleMPI()

# export the parfor function
parfor = smpi.parfor

# export the pprint function
pprint = smpi.pprint