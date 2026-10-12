import json, sys, numpy as np
sys.argv, argv = ['x'], sys.argv
exec(open('maze.py').read().split("if __name__")[0])
geom = json.load(open('geom.json')); net = argv[1]; x0b, y0b, x1b, y1b = map(float, argv[2:6]); pts = [tuple(map(float, p.split(','))) for p in argv[6:]]
T, V, g = raster(geom, net)
gx0, gy0 = g[0], g[1]
i0, i1, j0, j1 = int((x0b - gx0) / R), int((x1b - gx0) / R), int((y0b - gy0) / R), int((y1b - gy0) / R)
imgs = []
for l in (0, 1):
    img = np.full((j1 - j0, i1 - i0, 3), 255, np.uint8)
    img[T[l, j0:j1, i0:i1]] = (60, 60, 60)
    img[(~T[l, j0:j1, i0:i1]) & (V[0, j0:j1, i0:i1] | V[1, j0:j1, i0:i1])] = (200, 230, 255)
    for x, y in pts:
        jj, ii = int((y - gy0) / R) - j0, int((x - gx0) / R) - i0
        img[max(0, jj - 1):jj + 2, max(0, ii - 1):ii + 2] = (255, 0, 0)
    imgs.append(img)
img = np.concatenate([imgs[0], np.full((imgs[0].shape[0], 4, 3), 0, np.uint8), imgs[1]], axis=1)
open('v.ppm', 'wb').write(b'P6 %d %d 255\n' % (img.shape[1], img.shape[0]) + img.tobytes())
