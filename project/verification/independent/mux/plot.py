#!/usr/bin/env python3
"""Plot the TI simulated USB/solar handoff from the saved CSV; matplotlib required."""
import csv
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

here=Path(__file__).resolve().parent
with (here/'threshold_nominal.csv').open() as f:
    rows=list(csv.DictReader(f))
def series(key):return [float(row[key]) for row in rows]
t=[(s-.008)*1e6 for s in series('time_s')]
v=series('charger_input_V')
fig,ax=plt.subplots(figsize=(8,3.6),layout='constrained')
ax.axhspan(4.35,4.63,color='#d1aa63',alpha=.19,label='VINDPM BQ24074')
ax.plot(t,series('solar_at_mux_V'),color='#429272',lw=1.5,label='PV valid')
ax.plot(t,series('usb_at_mux_V'),color='#90959c',lw=1.5,linestyle='--',label='USB')
ax.plot(t,v,color='#123e65',lw=2,label='CHG_IN / ieșire mux')
idx=v.index(min(v));ax.plot(t[idx],v[idx],'o',color='#123e65',ms=4)
ax.annotate(f'{v[idx]:.3f} V',(t[idx],v[idx]),(t[idx]+28,v[idx]-.03),
            ha='left',va='top',fontsize=9,arrowprops=dict(arrowstyle='-',color='#123e65'))
ax.set(xlim=(-10,300),ylim=(3.45,5.4),xlabel='Timp de la începutul scăderii USB (µs)',ylabel='Tensiune (V)',
       title='Comutare USB → solar, simulare TPS2116 la 27 °C')
ax.legend(loc='lower left',ncols=2,fontsize=8,frameon=False)
ax.grid(axis='y',color='#d5d9dd',lw=.7);ax.set_axisbelow(True);ax.yaxis.set_major_locator(MultipleLocator(.4))
ax.spines[['top','right']].set_visible(False)
plt.savefig(here/'threshold.svg',metadata={'Date':None})
