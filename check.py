# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:35:14 2022

@author: pascharapun.j
"""

def check(a,b):
    if(a>=b):
        return True,a
    else:
        
        return False,a

abal = 401
amax = 600
abuy = 200

amtCheck = amax - abal

if(amtCheck>=abuy):
    print('Buy : ' , abuy)
else:
    print('Buy : ' , amtCheck)