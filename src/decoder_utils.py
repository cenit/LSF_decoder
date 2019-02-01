#!/usr/bin/env python

# -*- coding: utf8 -*-

"""
Module name: decoder_utils, based on dso200

dso200 is Copyright (c) 2014 Good Will Instrument Co., Ltd All Rights Reserved.
Copyright (c) 2019 Stefano Sinigardi, Coesia, All Rights Reserved.

This program is free software; you can redistribute it and/or modify it under the terms
of the GNU Lesser General Public License as published by the Free Software Foundation;
either version 2.1 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.
You can receive a copy of the GNU Lesser General Public License from http://www.gnu.org/
"""

import struct
import numpy as np
import array
import struct
import matplotlib.pyplot as plt
import os
import sys
import time

class Dso200:
  def __init__(self):
    self.iWave=[[], []]
    self.vdiv=[[], []]
    self.vunit=[[], []]
    self.dt=[[], []]
    self.vpos=[[], []]
    self.hpos=[[], []]
    self.ch_list=[]
    self.info=[[], []]

  def readRawDataFile(self,  fileName):
    self.info=[[], []]
    print("Opening ", fileName, " to read LSF data")
    f = open(fileName, 'rb')
    info = []

    # Read file header.
    infob=f.readline().split(b';')             #The last item will be b'\n' (the b is because the file is opened in binary mode).
    info = [x.decode('utf-8') for x in infob]  #decode the list from binary item to strings

    if(f.read(1)!=b'#'):
      print('Format error!')
      sys.exit(0)
    digit=int(f.read(1))
    num=int(f.read(digit))
    wave=f.read() #Read raw data from file.
    self.points_num=len(wave)/2   #Calculate sample points length.
    f.close()

    ch=0

    sCh=[s for s in info if "Source" in s]
    self.ch_list.append(sCh[0].split(',')[1])
    sVunit = [s for s in info if "Vertical Units" in s]
    self.vunit[ch] =sVunit[0].split(',')[1]      #Get vertical units.
    sDv = [s for s in info if "Vertical Scale" in s]
    self.vdiv[ch] = float(sDv[0].split(',')[1])  #Get vertical scale. => Voltage for ADC single step.
    sVpos=[s for s in info if "Vertical Position" in s]
    self.vpos[ch] =float(sVpos[0].split(',')[1]) #Get vertical position.
    sHpos = [s for s in info if "Horizontal Position" in s]
    self.hpos[ch] =float(sHpos[0].split(',')[1]) #Get horizontal position.
    sDt = [s for s in info if "Sampling Period" in s]
    self.dt[ch]=float(sDt[0].split(',')[1])      #Get sample period.
    dv1=self.vdiv[ch]/25
    vpos=int(self.vpos[ch]/dv1)+128
    num=int(self.points_num)
    for x in range(24):
      self.info[ch].append(info[x])
    self.info[ch].append('Mode,Fast')  #Convert info[] to csv compatible format.
    self.info[ch].append('Waveform Data')
    self.iWave[ch] = np.array(struct.unpack('<%sh' % (len(wave) // 2), wave))
    for x in range(num):               #Convert 16 bits signed number to floating point number.
      self.iWave[ch][x]-=vpos
    del wave
    return 1


class oscilloscope_data():
  def __init__(self, inputFileName, outputFileName, oldCSV=False, showPlot=False):
    self.inputFileName = inputFileName
    self.outputFileName = outputFileName
    self.oldCSV = oldCSV
    self.showPlot = showPlot
    self.dso = Dso200()

  def save_csv(self):
    num = len(self.dso.ch_list)
    for ch in range(num):
      if(self.dso.info[ch] == []):
        print('Failed to save data, raw data information is required!')
        return
    print("Opening ", self.outputFileName, " to write CSV data")
    f = open(self.outputFileName, 'w')
    item = len(self.dso.info[0])
    if (self.oldCSV):
      print("Using deprecated CSV file variant")
      #Write file header.
      f.write('%s,\r\n' % self.dso.info[0][0])
      for x in range(1,  25):
        str = ''
        for ch in range(num):
          str += ('%s,' % self.dso.info[ch][x])
        str += '\r\n'
        f.write(str)
      str = ''
      for ch in range(num):
        str += ('%s,' % self.dso.info[ch][25])
      str += '\r\n'
      f.write(str)
    else:
      print("Using modern CSV file variant")
    #Write raw data.
    item = len(self.dso.iWave[0])
    self.time = [[0] * item for i in range(num)]
    my_time = [0.0] * num
    for x in range(item):
      str = ''
      for ch in range(num):
        if (self.oldCSV):
          str += ('%s,' % self.dso.iWave[ch][x])
        else:
          self.time[ch][x] = my_time[ch]
          str += ('%s\t%s' % (self.time[ch][x], self.dso.iWave[ch][x]))
          my_time[ch] += self.dso.dt[ch]
      str += '\r\n'
      f.write(str)
    f.close()
    print('Done!')

  def load_lsf(self):
    self.dso.ch_list = []
    if os.path.exists(self.inputFileName):
      count = self.dso.readRawDataFile(self.inputFileName)
      if(count > 0):
        total_chnum = len(self.dso.ch_list)
        if(total_chnum == 0):
          print('No channel found in file, error!!')
          return
      else:
        print('Empty file!')
    else:
      print('File not found!')

  def show_plots(self):
    num = len(self.dso.ch_list)
    for ch in range(num):
      plt.plot(self.time[ch], self.dso.iWave[ch])
    plt.show()

  def run(self):
    self.load_lsf()
    self.save_csv()
    if self.showPlot:
      self.show_plots()
