import random
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
# queryGenerator.py                                                        #
# Takes a UDS file as an input and outputs a text file with newline        #
# separated queries.                                                       #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
# Takes two arguments:                                                     #
# "Filename" - The name of the file (without the .txt extension)           #
# "splitVal" - The size of the split to be making. Can either take a       #
#              number, or "rand", which is used to generate queries with   #
#              random lengths.
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
# Produces one output file:                                                #
#  The query file is a newline separated list of "words".                  #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
class queryGenerator:
    def __init__(self,filename,splitVal):
        self.file = filename   # Filename, durr
        self.randFlag = 0      # Flag for random use
        self.vIn = splitVal
        if(splitVal == "rand"):
            self.split = 0
            self.randFlag = 1
        else:
            self.split = int(splitVal)
        self.split = splitVal  # The length of queries we want
        self.queries = []      # The queries
        self.fileContents = "" # Contents of the file
        self.operations()

    # Logic stuff
    def operations(self):
        self.readFile()
        self.generateQueries()
        self.writeFile()

    # Generates the queries by splitting the UDS files
    def generateQueries(self):
        word = ""
        bit,i=0,0
        while i < len(self.fileContents):
            if self.randFlag == 1:
                self.split = random.randint(1,15)
            for j in range(i,i+self.split):
                if(j<len(self.fileContents)):
                    word += self.fileContents[j]
                # End If
            # End For
            if bit == 0:
                self.queries.append(word)
            # End If
            bit = abs(bit - 1)
            word = ""
            i+=self.split
        # End For
        print("Queries generated")

    # Read file
    def readFile(self):
        f = open(self.file+".txt",'r')
        contents = f.read()
        self.fileContents = contents
        f.close()
        print("File read")
        
    # Write file
    def writeFile(self):
        f = open(self.file+"_QUERY.txt",'w')
        for item in self.queries:
            f.write("%s\n"%item)
        f.close()
        print("File written")
