import simplempi
import pytest


@pytest.mark.parametrize("use_mpi", [True, False])
def test_scatter_list(use_mpi):
    """Test the scatter method on a list."""

    if use_mpi:
        from mpi4py import MPI

        comm = MPI.COMM_WORLD
    else:
        comm = None

    smpi = simplempi.simpleMPI(comm)

    # Make a list of things (20 numbers in this case)
    test_list = list(range(20))

    # Scatter the list to all processors (myList differs among processes now)
    my_list = smpi.scatter(test_list)

    # Print the list contents (as well as the rank of the printing process)
    smpi.pprint(my_list)
