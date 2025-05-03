import matplotlib.pyplot as plot

dpiVal = 150
fig = plot.figure(1, figsize=(8, 5), dpi=dpiVal)

#dilate by cube separated
IMG8bit =                   (0.00742482, 0.02106334)
IMG32bit =                  (0.00223300, 0.00574368)
BUF8bit =       (0.03253067, 0.11196576, 0.23860629, 0.44621034, 0.62068964)
BUF32bit =      (0.00824769, 0.02497671, 0.05927951, 0.10079227, 0.16485294)
BUF64bit =      (0.00452565, 0.01360407, 0.02870246, 0.05084363, 0.07892965)
Python =        (0.3560899877548218, 0.7002934336662292, 0.9978255200386047, 1.3822598147392273, 1.7004249954223633)
Matlab =        (0.88372150, 0.05201105, 0.30350415, 0.46292708, 0.64323076)
LeptonicaRas =              (0.00614377) #atualizar
LeptonicaDWA =              (0.01047654) #atualizar

#IMG8bit =      (0.00550548,0.04496613)
#IMG32bit =     (0.00153361,0.00503408)
#BUF8bit =      (0.02821969,0.11137216,0.25631316,0.46574795,0.723762)
#BUF32bit =     (0.00755548,0.02850228,0.06520954,0.11602245,0.1809226)
#BUF64bit =     (0.00366354,0.01295646,0.02856483,0.05019,0.07841731)
#Python =       (0.2360265,0.75432434,0.73625667,0.982544517,1.270084142)
#Matlab =       (0.040442,0.061566,0.578086,0.804873,1.156343)
#Matlab =        (0.79153498, 0.05051812, 0.28325248, 0.40520314, 0.50928588)
#LeptonicaRas = (0.006808123)
#LeptonicaDWA = (0.009720981)

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
line9 = plot.plot(dimensions2,  LeptonicaDWA, 'mv-')

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

legend = plot.legend((line1[0], line2[0], line3[0], line4[0], line5[0], line6[0], line7[0], line8[0], line9[0]),
 ('Python', 'MATLAB', 'VisionGL-BUF-8bit', 'VisionGL-BUF-32bit', 'VisionGL-BUF-64bit', 'VisionGL-IMG-8bit', 'VisionGL-IMG-32bit', 'Leptonica Rasterop', 'Leptonica DWA'),
                     bbox_to_anchor=[1.0, 1.017],
                     shadow=False, loc = 2, fontsize = 'medium')

#frame = legend.get_frame()
#frame.set_facecolor('1.0')
#for t in legend.get_texts():
    #t.set_fontsize(6)

plot.show()

fig.savefig('DilateByCubeSep.png', dpi=dpiVal)
