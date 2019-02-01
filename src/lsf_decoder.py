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

import decoder_utils as du
import argparse


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert LSF file to CSV')
  parser.add_argument('input_file', help='Input file (LSF format)')
  parser.add_argument('output_file', help='Output file (CSV format)')
  parser.add_argument('--oldCSV', dest='oldCSV', default=False, action='store_true', help='Use original CSV output format', required=False)
  parser.add_argument('--showPlot', dest='showPlot', default=False, action='store_true', help='Show the plot in a windows after conversion', required=False)
  args = parser.parse_args()
  if args.input_file is not None and args.output_file is not None:
    a = du.oscilloscope_data(inputFileName=args.input_file, outputFileName=args.output_file, oldCSV=args.oldCSV, showPlot=args.showPlot)
  else:
    parser.print_help()
  a.run()
