"""
takes the 4 graphs as picture and make a bigger picture
"""
import os
from skimage import io
import matplotlib.pyplot as plt

images = []
for path in os.listdir("img/authors_network_map"):
    img = io.imread('img/authors_network_map/' + path)
    images.append(img)

# fig, axes = plt.subplots(2, 2, figsize=(24, 24))
# ax = axes.ravel()

fig = plt.figure(figsize=(24, 24))
ax = [fig.add_subplot(2, 2, i + 1) for i in range(4)]

for a in ax:
    a.set_xticklabels([])
    a.set_yticklabels([])
    a.set_aspect('equal')

fig.subplots_adjust(wspace=0, hspace=0)

ax[0].imshow(images[0])
ax[0].set_title("CA_AI")
ax[1].imshow(images[1])
ax[1].set_title("LoL_AI")
ax[2].imshow(images[3])
ax[2].set_title("CA")
ax[3].imshow(images[2])
ax[3].set_title("LoL")
[axi.axis("off") for axi in ax]

plt.show()
fig.suptitle("Countries' publications and collaborations for two SDGs : Climate Action and Life on Land", fontsize=16)
fig.savefig('combine.jpeg')
