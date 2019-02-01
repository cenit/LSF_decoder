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

from PIL import Image
from struct import unpack
import numpy as np
import array
import struct
import os, sys, time

def generate_lut():
  global lu_table
  num=65536
  lu_table=[]
  for i in range(num):
    pixel888=[0]*3
    pixel888[0]=(i>>8)&0xf8
    pixel888[1]=(i>>3)&0xfc
    pixel888[2]=(i<<3)&0xf8
    lu_table.append(pixel888)

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
    generate_lut()

  def convertWaveform(self, ch, factor):
    dv=self.vdiv[ch]/25
    if(factor==1):
      num=self.points_num
      fWave=[0]*num
      for x in range(num):       #Convert 16 bits signed to floating point number.
        fWave[x]=float(self.iWave[ch][x])*dv
    else: #Reduced to helf points.
      num=self.points_num/factor
      fWave=[0]*num
      for x in range(num):       #Convert 16 bits signed to floating point number.
        i=factor*x
        fWave[x]=float(self.iWave[ch][i])*dv
    return fWave

  def readRawDataFile(self,  fileName):
    #Check file format(csv or lsf)
    self.info=[[], []]
    if(fileName.lower().endswith('.csv')):
      self.dataType='csv'
    elif(fileName.lower().endswith('.lsf')):
      self.dataType='lsf'
    else:
      return -1
    f = open(fileName, 'rb')
    info=[]
    #Read file header.
    if(self.dataType=='csv'):
      for x in range(26):
        info.append(f.readline().split(',\n')[0])
      if(info[0].split(',')[1]!='0.20'): #Check format version
        f.close()
        return -1
      count=info[5].count('CH')  #Check channel number in file.
      wave=f.read().splitlines() #Read raw data from file.
      self.points_num=len(wave)
    else:
      info=f.readline().split(';') #The last item will be '\n'.
      if(info[0].split('Format,')[1]!='0.20'): #Check format version
        f.close()
        return -1
      if(f.read(1)!='#'):
        print('Format error!')
        sys.exit(0)
      digit=int(f.read(1))
      num=int(f.read(digit))
      count=1
      wave=f.read() #Read raw data from file.
      self.points_num=len(wave)/2   #Calculate sample points length.
    f.close()

    if(count==1): #1 channel
      ch=0
      self.iWave[ch]=[0]*self.points_num
      sCh=[s for s in info if "Source" in s]
      self.ch_list.append(sCh[0].split(',')[1])
      sVunit = [s for s in info if "Vertical Units" in s]
      self.vunit[ch] =sVunit[0].split(',')[1]    #Get vertical units.
      sDv = [s for s in info if "Vertical Scale" in s]
      self.vdiv[ch] = float(sDv[0].split(',')[1])  #Get vertical scale. => Voltage for ADC's single step.
      sVpos=[s for s in info if "Vertical Position" in s]
      self.vpos[ch] =float(sVpos[0].split(',')[1]) #Get vertical position.
      sHpos = [s for s in info if "Horizontal Position" in s]
      self.hpos[ch] =float(sHpos[0].split(',')[1]) #Get horizontal position.
      sDt = [s for s in info if "Sampling Period" in s]
      self.dt[ch]=float(sDt[0].split(',')[1])    #Get sample period.
      dv1=self.vdiv[ch]/25
      vpos=int(self.vpos[ch]/dv1)+128
      num=self.points_num
      if(self.dataType=='csv'):
        for x in range(26):
          self.info[ch].append(info[x])
        for x in range(num):
          value=int(wave[x].split(',')[0])
          self.iWave[ch][x]=value
      else: #lsf file
        for x in range(24):
          self.info[ch].append(info[x])
        self.info[ch].append('Mode,Fast') #Convert info[] to csv compatible format.
        self.info[ch].append('Waveform Data')
        self.iWave[ch] = np.array(unpack('<%sh' % (len(wave)/2), wave))
        for x in range(num):      #Convert 16 bits signed number to floating point number.
          self.iWave[ch][x]-=vpos
      del wave
      return 1
    elif(count==2): #2 channel, csv file only.
      #write waveform's info to self.info[]
      for ch in range(count):
        self.info[ch].append(info[0])
      for x in range(1, 26):
        str=info[x].split(',')
        for ch in range(count):
          self.info[ch].append('%s,%s'%(str[2*ch],  str[2*ch+1]))
      for ch in range(count):
        self.iWave[ch]=[0]*self.points_num
        sCh=[s for s in info if "Source" in s]
        self.ch_list.append(sCh[0].split(',')[2*ch+1])
        sVunit = [s for s in info if "Vertical Units" in s]
        self.vunit[ch] =sVunit[0].split(',')[2*ch+1]    #Get vertical units.
        sDv = [s for s in info if "Vertical Scale" in s]
        self.vdiv[ch] = float(sDv[0].split(',')[2*ch+1])  #Get vertical scale. => Voltage for ADC's single step.
        sVpos=[s for s in info if "Vertical Position" in s]
        self.vpos[ch] =float(sVpos[0].split(',')[2*ch+1]) #Get vertical position.
        sHpos = [s for s in info if "Horizontal Position" in s]
        self.hpos[ch] =float(sHpos[0].split(',')[2*ch+1]) #Get horizontal position.
        sDt = [s for s in info if "Sampling Period" in s]
        self.dt[ch]=float(sDt[0].split(',')[2*ch+1])    #Get sample period.

      num=self.points_num
      for ch in range(count):
        self.iWave[ch]=[0]*num
      for i in range(num):
        str=wave[i].split(',')
        for ch in range(count):
          index=2*ch
          self.iWave[ch][i]=int(str[index])
    else:
      return -1

    del wave
    return count
