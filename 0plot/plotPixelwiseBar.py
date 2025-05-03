import numpy as np
import matplotlib.pyplot as plt

dpiVal = 150
fig = plt.figure(figsize=(8, 5), dpi=dpiVal)
ax = fig.add_subplot(111)

N = 5
#               (Thr, Not, Max, Copy, Unpack) 
IMG8bit =       (0.05050152, 0.00128979, 0.00167566, 0.00157540, 0.04150064)
IMG32bit =      (0.01096829, 0.00079215, 0.00105390, 0.00080320, 0.02295839)
#IMG32bit =      (0.01631428, 0.00082071, 0.00103096, 0.00180379, 0.01344529)
BUF8bit =       (0.07927493, 0.00095964, 0.00113753, 0.00091166, 0.10549264)

BUF32bit =      (0.00570503, 0.00026831, 0.00040521, 0.00029795, 0.00593040)
#BUF32bit =      (0.02186632, 0.00032746, 0.00050213, 0.00033384, 0.04502818)
BUF64bit =      (0.01151223, 0.00023502, 0.00035292, 0.00022596, 0.03331079)
Python =        (0.1632549,  0.4730299,  0.3754149,  0.1747599,  0.0)
Matlab =        (0.23627298, 0.00958959, 0.00588026, 0.01793810, 0.0) #3d
#Matlab =        (0.01924053, 0.01199060, 0.00553824, 0.01821740, 0.0) #3d

Leptonica =     (0.01537871, 0.00044592, 0.00182011, 0.00056607, 0.02834262)
#Leptonica =     (0.01910022, 0.00047179, 0.00123181, 0.00047916, 0.02629045)

##IMG8bit =      (0.00656199,0.00085386,0.00083002,0.00125941)
#IMG32bit =     (0.00572795,0.00026469,0.00048334,0.00035589,    0.01220367 )
##BUF8bit =      (0.010855,0.000197,0.000390,0.000185)
#BUF32bit =     (0.0054335,0.0002160,0.0002181,0.0002371,        0.0052687 )
##BUF64bit =     (0.0108552,0.0001966,0.0003905,0.0001845)
#Python =       (0.079676,0.040739,0.011411,0.010110, 0.0)
#Matlab =       (0.014531,0.009787,0.010120,0.011089, 0.0)
#Leptonica = (0.013076044,0.00061599,0.000786607,0.000194775,    0.001849225 )

bars4 = np.arange(4)
bars5 = np.arange(N)  # the x locations for the groups
width = 0.15      # the width of the bars

print(bars4)
print(bars5)

rectVisionGLimg = ax.bar(bars5 + width*1.5, IMG32bit, width, color='c')
rectVisionGLbuf = ax.bar(bars5 + width*2.5, BUF32bit, width, color='b')
rectLeptonica   = ax.bar(bars5 + width*3.5, Leptonica, width, color='m')
rectPython      = ax.bar(bars5 + width*4.5, Python, width, color='g')
rectMatlab      = ax.bar(bars5 + width*5.5, Matlab, width, color='r')
#rectEmpySpace = ax.bar(ind + width*3, emptySpace, width, color='w')

# add some text for labels, title and axes ticks
#ax.set_xlim(-width, len(ind)+width)
ax.set_ylabel('Time(s)')
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
#plt.title('Other operations', weight='bold')
ax.set_xticks(bars5 + width*2.5)
ax.set_yscale('log')
ax.set_ylim(1e-4, 1e1)
xtickNames = ax.set_xticklabels(('Threshold', 'Not', 'Max', 'Copy', 'Unpack'))
plt.setp(xtickNames, rotation=10, fontsize=12)
legend = ax.legend((rectVisionGLimg[0], rectVisionGLbuf[0], rectLeptonica[0], rectPython[0], rectMatlab[0]),
                   ('VisionGL-IMG-32bit', 'VisionGL-BUF-32bit', 'Leptonica', 'Python', 'MATLAB'),
                   bbox_to_anchor=[0.95, 1.21],
                   shadow=False, loc = 1, fontsize = 'medium', ncol=3)

#ax.legend((rectVisionGL[0], rectPython[0]), ('VisionGL', 'Python'))


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.5f' % float(height),
                ha='center', va='bottom', rotation=90)

autolabel(rectVisionGLimg)
autolabel(rectVisionGLbuf)
autolabel(rectPython)
autolabel(rectMatlab)
autolabel(rectLeptonica)

box = ax.get_position();
ax.set_position([box.x0, box.y0, box.width, box.height*0.9])

plt.show()

fig.savefig('PixelwiseBar.png', dpi=dpiVal)
