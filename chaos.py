import numpy as np

def generate_attractor(n, seed = None):
    vertices = np.array([[0, 1],
                         [np.cos(7*np.pi/6), np.sin(7*np.pi/6)], 
                         [np.cos(11*np.pi/6), np.sin(11*np.pi/6)]])
    
    np.random.seed(seed)
    indices = np.random.randint(0, 3, size = n)

    points = np.zeros((n, 2))
    for i in range(1, n):
        points[i] = (points[i-1] + vertices[indices[i]]) / 2

    return points