#!/usr/bin/env python3
 
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
 
fig = plt.figure()
plt.axis([0, 8, 0, 20])
plt.xlabel('pořadí')
plt.ylabel('přirozená čísla')
 
images = []
for i,x in enumerate([2, 3, 5, 7, 11, 13, 17], start=1):
    img = plt.plot(i, x, 'ro')
    images.append(img)
 
animation = ArtistAnimation(fig, images)
print('Kroků animace:', len(images))
animation.save('anim-01.mp4')
 
plt.show()
