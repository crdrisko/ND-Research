#!/bin/bash
# Copyright (c) 2010 Chris Johnson. Some rights reserved.
# Licensed under the Freeware License. See the LICENSE file in the project root for more information.
#
# Name: Listing7_03.sh
# Author: crdrisko
# Date: 07/03/2019-09:46:41
# Description: Reverse the order of a string: store result in _REVSTR

_revstr()   #@USAGE: _revstr STRING
{
    var=$1
    _REVSTR=
    while [ -n "$var" ]
    do
        temp=${var%?}
        _REVSTR=$_REVSTR${var#"$temp"}
        var=$temp
    done
}
