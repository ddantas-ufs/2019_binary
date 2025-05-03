import numpy as np
import matplotlib.pyplot as plt

dpiVal = 150
fig = plt.figure(figsize=(8, 5), dpi=dpiVal)
ax = fig.add_subplot(111)

N = 3
#      ('Upload', 'Download', 'BinSwap')
IMG = (0.00129985, 0.00139951, 0.00082964)
BUF = (0.00130004, 0.00151387, 0.00081567)
#IMG = (0.00191908, 0.00179078, 0.00087146)
#BUF = (0.00108329, 0.00114035, 0.00156112)

#      ('Upload', 'Download', 'BinToGray' , 'BinSwap')
#IMG = (0.00093049,0.00142192,0.01220367,0.0006982)
#BUF = (0.00083892,0.00323197,0.0052687,0.0007447)

ind = np.arange(N)  # the x locations for the groups
width = 0.3      # the width of the bars

rectVisionGLimg = ax.bar(ind + width*1.5, IMG, width, color='c')
rectVisionGLbuf = ax.bar(ind + width*2.5, BUF, width, color='b')
#rectEmpySpace = ax.bar(ind + width*3, emptySpace, width, color='w')

# add some text for labels, title and axes ticks
#ax.set_xlim(-width, len(ind)+width)
ax.set_ylabel('Time(s)')
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
#plt.title('Other operations', weight='bold')
ax.set_xticks(ind + width*2.5)
ax.set_yscale('log')
ax.set_ylim(1e-4, 1e1)
xtickNames = ax.set_xticklabels(('Upload', 'Download', 'BinSwap'))
plt.setp(xtickNames, rotation=10, fontsize=12)
legend = ax.legend((rectVisionGLimg[0], rectVisionGLbuf[0]),
                   ('VisionGL-IMG-32bit', 'VisionGL-BUF-32bit'),
                   bbox_to_anchor=[0.90, 1.15],
                   shadow=False, loc = 1, fontsize = 'medium', ncol=2)

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

box = ax.get_position();
ax.set_position([box.x0, box.y0, box.width, box.height*0.9])

plt.show()

fig.savefig('VisionglBar.png', dpi=dpiVal)
