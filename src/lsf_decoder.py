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


if __name__ == '__main__':
  a = du.oscilloscope_data()
  a.run()
