#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
input_file = open("./layout.csv", "r")
x = []
y = []
is_head = True
for _ in input_file.readlines():
    if (is_head):
        is_head = False
        continue
    t = _.strip()
    t = t.split(',')
    x.append(float(t[1]))
    y.append(float(t[2]))
input_file.close()

plt.scatter(x, y, s=5.0)
ax = plt.gca()
ax.set_aspect(1)
plt.show()
