#!/bin/bash
# Copyright (c) 2010 Chris Johnson. Some rights reserved.
# Licensed under the Freeware License. See the LICENSE file in the project root for license information.
#
# Name: bpl_l.sh - (Listing 11-5)
# Author: Cody R. Drisko (crdrisko)
# Date: 07/18/2019-07:49:46
# Description: List files in long format, piped through less

bpl_l()
{
    ls -lA "$@" | less      ## the -A option is specific to GNU and *BSD versions
}
