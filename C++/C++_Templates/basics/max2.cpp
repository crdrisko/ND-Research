// Copyright (c) 2017 by Addison-Wesley, David Vandevoorde, Nicolai M. Josuttis, and Douglas Gregor. All rights reserved.
//
// Name: max2.cpp - Version 1.0.0
// Author: cdrisko
// Date: 07/26/2020-08:03:17
// Description: Overloading a function template

// maximum of two int values:
int max(int a, int b)
{
    return b < a ? a : b;
}

// maximum of two values of any type:
template<typename T>
T max(T a, T b)
{
    return b < a ? a : b;
}

int main()
{
    ::max(7, 42);                           // calls the nontemplate for two ints
    ::max(7.0, 42.0);                       // calls max<double> (by argument deduction)
    ::max('a', 'b');                        // calls max<char> (by argument deduction)
    ::max<>(7, 42);                         // calls max<int> (by argument deduction)
    ::max<double>(7, 42);                   // calls max<double> (no argument deduction)
    ::max('a', 42.7);                       // calls the nontemplate for two ints
}
