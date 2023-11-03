class simpleMPI:
    """A simple wrapper around mpi4py that offers simple scattering of a list of
    objects.

    This is useful for embarassingly parallel, SPMD, type tasks that simply need
    to work on a list of things.

    example usage:

        import simpleMPI

        #Initialize MPI
        smpi = simpleMPI.simpleMPI()

        #Make a list of things (20 numbers in this case)
        test_list = list(range(20))

        #Scatter the list to all processors (myList differs among processes now)
        my_list = smpi.scatter(test_list)

        #Print the list contents (as well as the rank of the printing process)
        smpi.pprint(my_list)
    """

    def __init__(self, useMPI=True, comm=None):
        """A simple wrapper around mpi4py that offers simple scattering of a
        list of objects.

        input:
        ------

        useMPI      :   flag whether to use mpi4py (False is useful for
                        use/debugging in situations where mpi4py is unavailable)

        comm        :   MPI communicator to use (if None, use MPI.COMM_WORLD)

        """

        # Save whether we are using MPI
        self.useMPI = useMPI

        # If MPI is being used, initialize it and save the number of
        # processors/processor size
        if useMPI:
            if comm is None:
                # Initialize MPI
                from mpi4py import MPI

                # Get the global communicator
                comm = MPI.COMM_WORLD

            # Get this processes's rank
            rank = comm.Get_rank()
            # Get the total number of processors
            mpisize = comm.Get_size()

        # If MPI isn't being used, simply set mpisize to 1 and set dummy values
        # for comm and rank
        else:
            comm = 0
            rank = 0
            mpisize = 1

        # Save the MPI paramters to the class
        self.comm = comm
        self.rank = rank
        self.mpisize = mpisize

        return

    def sync_barrier(self):
        """Sets a synchronization barrier."""
        if self.useMPI:
            self.comm.Barrier()

        return

    def scatter(self, iterable):
        """Scatter a list of objects to all participating processors."""
        if self.useMPI:
            # If this is the root processor, divide the list as evenly as
            # possible among processors
            # _divide_list_for_scattering() returns a list of lists, with `mpisize`
            # lists in the top level list
            if self.rank == 0:
                try:
                    scatterable = self._divide_list_for_scattering(iterable)
                except KeyError:
                    scatterable = self._divide_dict_for_scattering(iterable)
            else:
                scatterable = None

            # Scatter the lists to the other processes
            myList = self.comm.scatter(scatterable, root=0)
        else:
            # If we aren't using MPI, simply return the given list
            myList = iterable

        # Return this processor's list
        return myList

    def parfor(self, iterable):
        """A wrapper around simpleMPI.scatter() designed to be used in a loop

        input:
        ------

            iterable    :   list of objects to work on

        output:
        -------

            outlist     :   list of objects returned by the function

        """

        # Return the list
        return self.scatter(iterable)

    def _divide_list_for_scattering(self, iterable):
        """returns a list of lists, with `self.mpisize` lists in the top level list"""

        # Create a list that explicitly has the proper size
        outlist = [[] for i in range(self.mpisize)]

        n = 0
        # Go through each item in the input list and append it to the output list
        # Cycle through the indices of the output list so that they input list is
        # dividided as evenly as possible
        for i in range(len(iterable)):
            outlist[n].append(iterable[i])
            n = n + 1
            if n >= self.mpisize:
                n = 0

        # Return the list
        return outlist

    def _divide_dict_for_scattering(self, indict):
        """returns a list of dicts, with `self.mpisize` lists in the top level list"""

        # Create a list that explicitly has the proper size
        outlist = [{} for i in range(self.mpisize)]

        n = 0

        # Go through each item in the input list and append it to the output list
        # Cycle through the indices of the output list so that they input list is
        # dividided as evenly as possible
        for item in indict:
            outlist[n][item] = indict[item]
            n = n + 1
            if n >= self.mpisize:
                n = 0

        # Return the list
        return outlist

    def pprint(self, *msg, **kwargs):
        """Does a parallel-friendly print (with information about the printing
        processor)"""
        print(
            "(rank {}/{}): ".format(self.rank + 1, self.mpisize), *msg, **kwargs
        )

    def print(self, *msg, **kwargs):
        """Does a parallel-friendly print (with information about the printing
        processor)"""
        self.pprint(*msg, **kwargs)
