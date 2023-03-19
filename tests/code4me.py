'''
 frames = []
    for t in range(14):
        image = imageio.v2.imread(f'./img/img_{t}.png')
        frames.append(image)
    imageio.mimsave('./example.gif',  # output gif
                    frames,  # array of input frames
                    fps=5)  # optional: frames per second
'''


def random_point(size):
    _x = random.randint(0, size)
    _y = random.randint(0, size)
    return (_x, _y)



'''
       seed option to show:
       MAX_RADIUS = 150  # MAX radius size

       - 80 - to movie
       - 9
       - 90
       - 199 - special case
       - 50 nice
       - 95 BUG NEED TO UNDERSTAND

       MAX_RADIUS = 30  # MAX radius size
       '''