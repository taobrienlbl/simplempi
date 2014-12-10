
class simpleMPI:

    def __init__(   self, \
                    useMPI = True):

        self.useMPI = useMPI

        if(useMPI):
          from mpi4py import MPI
          #Initialize MPI
          comm = MPI.COMM_WORLD
          rank = comm.Get_rank()
          mpisize = comm.Get_size()
        else:
          comm = 0
          rank = 0
          mpisize = 1

        self.comm = comm
        self.rank = rank
        self.mpisize = mpisize

    def doSyncBarrier(self):
      self.comm.Barrier()
      return

    def scatterList(self,inlist):
        """Scatter a list of objects to all participating processors."""
        if(self.useMPI):
          if self.rank == 0:
            scatterableList = self._divideListForScattering(inlist)
          else:
            scatterableList = None

          #Scatter the file list to the other processes
          myList = self.comm.scatter(scatterableList,root=0)
        else:
          myList = inlist

        return myList

    def _divideListForScattering(self,inlist):
      #Create a list that explicitly has the proper size
      outlist = [ [] for i in range(self.mpisize) ]

      n = 0
      #Go through each item in the input list and append it to the output list
      #Cycle through the indices of the output list so that they input list is
      #dividided as evenly as possible
      for i in range(len(inlist)):
        outlist[n].append(inlist[i])
        n = n + 1
        if(n >= self.mpisize):
          n = 0

      #Return the list
      return outlist

    def pprint(self,message):
        print("(rank {}/{}): {}".format(self.rank+1,self.mpisize,message))


if __name__ == "__main__":

    smpi = simpleMPI()

    testList = range(20)

    myList = smpi.scatterList(testList)

    smpi.pprint(myList)


