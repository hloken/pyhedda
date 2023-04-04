import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def create_images(x, y, x_celler, y_celler):
    fig, ax = plt.subplots()
    plt.axis("off")
    imgs = []
    for n, (i, j) in enumerate(zip(x, y)):
        print(n, i, j)
        R = np.zeros((x_celler, y_celler))
        
        for k, l in zip(i, j):
            R[k, l] = 1

        if n == 0:
            imgs.append([ax.imshow(R.T, cmap="gray")])
        else:
            imgs.append([ax.imshow(R.T, animated=True, cmap="gray")])
    return fig, ax, imgs


def create_animation(fname, x_celler, y_celler, x, y, fps=60):
    fig, ax, imgs = create_images(x=x, y=y, x_celler=x_celler, y_celler=y_celler)
    ani = animation.ArtistAnimation(fig, imgs, blit=True)
    ani.save(fname, fps=fps, writer="ffmpeg")
    plt.close()




