#!/bin/bash
# Copyright (c) 2010 Chris Johnson. Some rights reserved.
# Licensed under the Freeware License. See the LICENSE file in the project root for license information.
#
# Name: bpl_k.sh - (Listing 11-14)
# Author: Cody R. Drisko (crdrisko)
# Date: 07/18/2019-07:51:03
# Description: List commands whose short descriptions include a search string

bpl_k()     #@ USAGE: k string
{
    man -k "$@" | grep '(1'
}
