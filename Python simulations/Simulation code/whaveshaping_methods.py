# -*- coding: utf-8 -*-
"""
Created on Fri May 19 11:33:31 2023

@author: eliot
"""

a, b, c, n = 1.0377458446300538, 0.8923316798423064, 2.477346377606484, 3.1340306238829987

def output_static(x, a=a, b=b, c=c, n=n):
     y = x*a/((1+abs(c*x)**n)**(b/n))
     return y
