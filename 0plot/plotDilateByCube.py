import matplotlib.pyplot as plot

dpiVal = 150
fig = plot.figure(1, figsize=(8, 5), dpi=dpiVal)

#dilate by cube
IMG8bit =       (0.00711705, 0.02598773)
IMG32bit =      (0.00205253, 0.00663053)
BUF8bit =       (0.03240041, 0.14623527, 0.60458914, 2.57968032, 8.81732029)
BUF32bit =      (0.00785150, 0.03380073, 0.16008432, 0.60975623, 2.37709254)
BUF64bit =      (0.00419163, 0.01828698, 0.07549010, 0.29976418 ,1.13051202)
Python =        (0.32393285274505615, 0.5278900098800659, 1.0321751570701599, 2.275040214061737, 5.835061910152435)
Matlab =        (0.69974955, 0.02458588, 0.31233568, 0.44769138, 0.65478397)
LeptonicaRas =  (0.01827912) #atualizar

#IMG8bit =      (0.00579816,0.04965152)
#IMG32bit =     (0.00154023,0.00621684)
#BUF8bit =      (0.02852944,0.14128271,0.61469852,3.33720798,9.091652)
#BUF32bit =     (0.00755936,0.0365209,0.14919354,0.61795888,2.2634829)
#BUF64bit =     (0.00402706,0.01705139,0.07456492,0.29608025,1.1125946)
#Python =       (0.23102164, 0.281169342, 0.34057691, 0.367808628, 0.453035926)
#Matlab =       (0.041100, 0.028352, 0.176465, 0.451514, 0.598542)
#Matlab =        (0.66344248, 0.02478991, 0.29154615, 0.37500082, 0.49259183)
#LeptonicaRas = (0.006808123)

dimensions = (1, 2, 3, 4, 5)
dimensions23 = (2, 3)
dimensions2 = (2)
dimensions_label = ('1D', '2D', '3D', '4D', '5D')

plot.xticks(dimensions, dimensions_label)

line1 = plot.plot(dimensions,   Python, 'gd-')
line2 = plot.plot(dimensions,   Matlab, 'rs-')
line3 = plot.plot(dimensions,   BUF8bit, 'bo:')
line4 = plot.plot(dimensions,   BUF32bit, 'bo--')
line5 = plot.plot(dimensions,   BUF64bit, 'bo-')
line6 = plot.plot(dimensions23, IMG8bit, 'c*:')
line7 = plot.plot(dimensions23, IMG32bit, 'c*--')
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

fig.savefig('DilateByCube.png', dpi=dpiVal)
