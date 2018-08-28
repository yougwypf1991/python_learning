#!/usr/bin/env python3

class ClasTest():
    def __call__(self, a, b):
        print('Test!!!')
        print('a =', a, 'b = ', b)
        

test = ClasTest()
test(1, 2)