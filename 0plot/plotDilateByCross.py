import matplotlib.pyplot as plot

dpiVal = 150
fig = plot.figure(1, figsize=(8, 5), dpi=dpiVal)

#dilate by cross
IMG8bit =                   (0.00551308, 0.02313106)
IMG32bit =                  (0.00154995, 0.00623527)
BUF8bit =       (0.03251089, 0.08281183, 0.15976093, 0.28322852, 0.36504233)
BUF32bit =      (0.00820932, 0.02028681, 0.04186532, 0.06758423, 0.10193492)
BUF64bit =      (0.00441488, 0.01075734, 0.02079287, 0.03301833, 0.04790512)
Python =        (0.34746033668518066, 0.5004199552536011, 0.9846941947937012, 2.1999544215202332, 5.820089416503906)
Matlab =        (0.70207708, 0.02233689, 0.16917769, 0.45961484, 0.66128199)
LeptonicaRas =              (0.00869574) #atualizar

#IMG8bit =      (0.0043025,0.04957474)
#IMG32bit =     (0.00124244,0.00583096)
#BUF8bit =      (0.029299,0.083009,0.17157853,0.29733391,0.406817)
#BUF32bit =     (0.007507,0.021630,0.04334165,0.07306389,0.1059525)
#BUF64bit =     (0.003951,0.009950,0.01989383,0.03281472,0.04862003)
#Python =       (0.23212277,0.26385324,0.277716541,0.303491258,0.352338647)
#Matlab =       (0.043081,0.036432,0.433197,0.550197,0.702172)
#Matlab =        (0.69199225, 0.02238891, 0.30034579, 0.37004804, 0.51102840)
#LeptonicaRas = (0.005701687)

dimensions = (1, 2, 3, 4, 5)
dimensions23 = (2, 3)
dimensions2 = (2)
dimensions_label = ('1D', '2D', '3D', '4D', '5D')

plot.xticks(dimensions, dimensions_label)

line1 = plot.plot(dimensions,   Python, 'gd-')
line2 = plot.plot(dimensions,   Matlab, 'rs-')
line3 = plot.plot(dimensions,   BUF8bit, 'b*:')
line4 = plot.plot(dimensions,   BUF32bit, 'b^--')
line5 = plot.plot(dimensions,   BUF64bit, 'bs-')
line6 = plot.plot(dimensions23, IMG8bit, 'c*:')
line7 = plot.plot(dimensions23, IMG32bit, 'c^--')
line8 = plot.plot(dimensions2,  LeptonicaRas, 'mh-')

ax = plot.subplot(111)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)


plot.yscale('log')
ax.set_ylim(1e-3, 1e1)
plot.xlabel("Image Dimension", fontsize="large")
plot.ylabel("Time(s)", fontsize="large")

#plot.title('Convolution', weight='bold')
plot.grid(True, axis='both')

box = ax.get_position();
ax.set_position([box.x0, box.y0, box.width * 0.72, box.height]);

legend = plot.legend((line1[0], line2[0], line3[0], line4[0], line5[0], line6[0], line7[0], line8[0]),
                     ('Python', 'MATLAB', 'VisionGL-BUF-8bit', 'VisionGL-BUF-32bit', 'VisionGL-BUF-64bit', 'VisionGL-IMG-8bit', 'VisionGL-IMG-32bit', 'Leptonica Rasterop'),
                     bbox_to_anchor=[1.0, 1.017],
                     shadow=False, loc = 2, fontsize = 'medium')

#frame = legend.get_frame()
#frame.set_facecolor('1.0')
#for t in legend.get_texts():
    #t.set_fontsize(6)

plot.show()

fig.savefig('DilateByCross.png', dpi=dpiVal)
