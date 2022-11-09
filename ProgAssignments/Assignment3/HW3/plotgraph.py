import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
## pass a string from command line, indicating file name

#parser = argparse.ArgumentParser ()
# add optional arguments
#args = parser.parse_args ()


fig, ax = plt.subplots(figsize=[18,10])
topo = ["single", "linear", "tree"]
ax.plot(topo, [93.5923,103.2881,123.3581], c='r', marker="o", label='ABP')
ax.plot(topo, [92.5652,94.7035,108.4227], c='g', marker="o", label='Go-Back-N')
ax.plot(topo, [29.7405,31.2640,40.0225], c='b', marker="o", label='Selective Repeat')
plt.xticks(np.arange(0,3), topo, fontsize=10)
ax.set_xlabel('Topology')
ax.xaxis.set_label_coords(.5,-.1)
ax.set_ylabel('Latency of 10 epoch')
plt.title("A Comparison btwn ABP/GBN/SR")
plt.legend()
plt.savefig('HW3.png')
plt.show()
