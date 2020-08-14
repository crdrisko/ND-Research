#!/bin/bash
# Copyright (c) 2010 Chris Johnson. Some rights reserved.
# Licensed under the Freeware License. See the LICENSE file in the project root for license information.
#
# Name: linkBashful.sh - (Listing 12-9)
# Author: Cody R. Drisko (crdrisko)
# Date: 07/22/2019-08:27:27
# Description: Make multiple links to bashful script

cd "$HOME/bin" &&
for name in sleepy sneezy grumpy dopey
do
    ln -s bashful "$name"           ## you can leave out the -s option if you like
done
