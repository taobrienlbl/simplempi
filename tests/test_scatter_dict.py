import simplempi
import pytest


@pytest.mark.parametrize("use_mpi", [True, False])
def test_scatter_dict(use_mpi):
    """Test the scatter method on a dict"""

    if use_mpi:
        from mpi4py import MPI

        comm = MPI.COMM_WORLD
    else:
        comm = None

    smpi = simplempi.simpleMPI(comm)

    # Test scattering a dict object
    test_dict = {"a": 1, "b": 10, "c": "a string"}

    # Scatter the dict
    my_dict = smpi.scatter(test_dict)

    # Print the dict contents and the rank
    smpi.pprint(my_dict)
