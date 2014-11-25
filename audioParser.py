import wave, struct, scipy
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

# https://docs.python.org/3/library/wave.html#wave.Wave_read.close

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
# audioParser.py                                                           #
# Takes as an input a mono-channel, 44.1KHz .wav file and returns a "UDS"  #
# file. A UDS file is a text file containing four characters, "B","U","D", #
# and "S", which relate the current sample to the previous sample.         #
#                                                                          #
# To cut down on complexity, the program can also reduce the resolution of #
# the audio file by instead opting to sample every "reduceBy" samples.     #
# This cuts down on the total number of required comparisons, and may      #
# yield more accurate results.                                             #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
# Takes five arguments:                                                    #
# "filename"    - The name of the .WAV file to be parsed. ".wav" is added  #
#               - automatically.                                           #
# "reduceBy"    - The reduction in sampling, equivelant to len / reduceBy  #
#               - eg: reduceBy 16 = 1/16th the resolution of samples.      #
# "percentDiff" - The minimum percent difference between two samples to be #
#                 considered different                                     #
# "maximum"     - The length of the desired output in seconds              #
#               - I've just been using 15 seconds                          #
# "method"      - Used to chose the PREV or AVG method in reduction.       #
#               - Use 1 for the AVG method and anything other than 1 for   #
#               - PREV.                                                    #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
# Produces three output files:                                             #
# "[SONG]_reduced_R#_M#.wav" - The reduced version of the song, cut to     #
#                            - the selected length.                        #
#                            - R=reducedBy, M=method (1:avg, 0:prev        #
# "[SONG]_UDS_R#_M#_D#.txt"  - The UDS file with "U,D,S,B" characters.     #
#                            - R=reducedBy, M=method, D=percentDiff        #
# "[SONG]_UDS_R#_M#_D#.wav"  - A version of the song created using the UDS #
#                            - information.                                #
#                            - R=reducedBy, M=method, D=percentDiff        #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
class audioParser:
    def __init__(self,filename,reduceBy,percentDiff,maximum,method):
        self.file = filename
        self.reducer = reduceBy
        self.maxLen = maximum
        self.minDiff = percentDiff
        self.rate = 0
        self.reduceMethod = method
        self.data = []
        self.dataReduced = []
        self.UDS = []
        self.dataUDS = []
        self.operations()

    # Logic stuff
    def operations(self):
        self.readWavFile()
        if(self.reduceMethod == 1):
            self.reduceWavFileAvg()
        else:
            self.reduceMethod = 0
            self.reduceWavFilePrev()
        self.produceUDSfile()
        self.writeWavFile()
        #self.writeUDSwav()

    # Produces the UDS file. UDS stands for "Up, Down, Same", and records
    # whether or not a given sample has a higher, lower, or equal value to
    # the previous sample to some percentage of difference. 
    def produceUDSfile(self):
        prevLevel = self.dataReduced[0]
        self.UDS.append("B")
        i = 0
        while i < len(self.dataReduced):
            curLevel = self.dataReduced[i]
            curLevel += 0.00001
            perDiff = abs(((float(prevLevel) - float(curLevel)) / (float(curLevel)))*100)
            if perDiff < self.minDiff:
                self.UDS.append("S")
                for x in range(0,self.reducer):
                    self.dataUDS.append(prevLevel)
            elif prevLevel > curLevel:
                self.UDS.append("D")
                for x in range(0,self.reducer):
                    self.dataUDS.append(curLevel)   
            else:
                self.UDS.append("U")
                for x in range(0,self.reducer):
                    self.dataUDS.append(curLevel)
            prevLevel = curLevel
            i+=self.reducer
        print("Projected: %d, Actual: %d"%((len(self.data)/self.reducer),len(self.UDS)))
        f = open(self.file+"_UDS_R%d_M%d_D%d.txt"%(self.reducer,self.reduceMethod,self.minDiff),"w")
        for i in range(0,len(self.UDS)):
            f.write(self.UDS[i])
        f.close()
            
    # Reduces the audio file's complexity by writing every self.reducer number
    # at each step
    # Sounds better, may yield worse results
    def reduceWavFilePrev(self):
        prevI = 0
        for i in range(0,len(self.data)):
            if i%self.reducer == 0:
                self.dataReduced.append(self.data[i])
                prevI = i
            else:
                self.dataReduced.append(self.data[prevI])
        print(".WAV file reduced via 'Prev' mechanism")

    # Reduces the audio file's complexity by writing the average of self.reducer
    # numbers at each step
    # Sounds worse, may yield better results
    def reduceWavFileAvg(self):
        avg = 0
        for i in range(0,len(self.data)):
            if i%self.reducer == 0:
                avg += self.data[i]
                avg = avg / self.reducer
                for x in range(0,self.reducer):
                    self.dataReduced.append(avg)
                avg = 0
            else:
                avg += self.data[i]
        print(".WAV file reduced via 'Avg' mechanism")

    # Reads the .WAV file and trims it to the maximum length
    def readWavFile(self):
        self.rate, dataWhole = wavfile.read(self.file+".wav")
        dataWhole = dataWhole
        numSamples = self.maxLen * 44100
        for i in range(0,numSamples):
            self.data.append(dataWhole[i])
        print(".WAV file read. Rate = %d, Length = %d"%(self.rate,len(self.data)))

    # Writes a .WAV file with the UDS information
    def writeUDSwav(self):
        wavfile.write(self.file+"_UDS_R%d_M%d_D%d.wav"%(self.reducer,self.reduceMethod,self.minDiff),self.rate,np.asarray(self.dataUDS))
        print("UDS .WAV file written")

    # Write's the reduced .WAV file
    def writeWavFile(self):
        wavfile.write(self.file+"_reduced_R%d_M%d.wav"%(self.reducer,self.reduceMethod),self.rate,np.asarray(self.dataReduced))
        print("Reduced .WAV file written")
