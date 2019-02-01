#!/usr/bin/env python

# -*- coding: utf8 -*-

"""
Program name: lsf_decoder, based on OpenWave-200
OpenWave-200 is Copyright (c) 2014 Good Will Instrument Co., Ltd All Rights Reserved.
Copyright (c) 2019 Stefano Sinigardi, Coesia, All Rights Reserved.

This program is free software; you can redistribute it and/or modify it under the terms
of the GNU Lesser General Public License as published by the Free Software Foundation;
either version 2.1 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.
You can receive a copy of the GNU Lesser General Public License from http://www.gnu.org/
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy as np
import os, sys, time
import decoder_utils

class oscilloscope_data():
  def __init__(self, parent=None):
    self.figure = plt.figure()
    self.figure.set_facecolor('white')
    self.typeFlag = True  # Initial state -> Get raw data

  def save_csv(self):
    if(self.typeFlag==True): #Save raw data to csv file.
      file_name="test.csv"
      num=len(dso.ch_list)
      for ch in range(num):
        if(dso.info[ch]==[]):
          print('Failed to save data, raw data information is required!')
          return
      f = open(file_name, 'wb')
      item=len(dso.info[0])
      #Write file header.
      f.write('%s,\r\n' % dso.info[0][0])
      for x in range(1,  25):
        str=''
        for ch in range(num):
          str+=('%s,' % dso.info[ch][x])
        str+='\r\n'
        f.write(str)
      str=''
      if(num==1):
        str+=('%s,' % dso.info[0][25])
      else:
        for ch in range(num):
          str+=('%s,,' % dso.info[ch][25])
      str+='\r\n'
      f.write(str)
      #Write raw data.
      item=len(dso.iWave[0])
      tenth=int(item/10)
      n_tenth=tenth-1
      percent=10
      for x in range(item):
        str=''
        if(num==1):
          str+=('%s,' % dso.iWave[0][x])
        else:
          for ch in range(num):
            str+=('%s,,' % dso.iWave[ch][x])
        str+='\r\n'
        f.write(str)
        if(x==n_tenth):
          n_tenth+=tenth
          print('%3d %% Saved\r'%percent),
          percent+=10
      f.close()

  def load_lsf(self):
    dso.ch_list=[]
    sFileName="test.lsf"
    if os.path.exists(sFileName):
      print('Reading file...')
      count=dso.readRawDataFile(sFileName)
      #Print diagnostic data
      if(count>0):
        total_chnum=len(dso.ch_list)
        if(total_chnum==0):
          return
        print(total_chnum)
    else:
      print('File not found!')

if __name__ == '__main__':
  dso=decoder_utils.Dso200()
  main = oscilloscope_data()
  main.load_lsf()
  main.save_csv()
