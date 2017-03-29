
import numpy as np
import matplotlib
import matplotlib.pyplot as pp
import multiprocessing

def compute_mandel_numpy(c,maxit=256):
    escaped = np.full_like(c,np.inf,'d')
    z = np.zeros_like(c,'c16')
    
    for it in range(1,maxit):
        z = np.where(escaped == np.inf,z**2 + c,0)        
        escaped[np.abs(z) > 2.0] = it

    return escaped

def run_mandel_mp(extent=[-2.0,1.0,-1.25,1.25],res=256,maxit=256):
    xs = np.linspace(extent[0],extent[1],res)
    ys = np.linspace(extent[2],extent[3],res)
    
    c = xs[:,np.newaxis] + 1j*ys[np.newaxis,:]

    chunksize = 32
    
    pool = multiprocessing.Pool(processes=4)
    escaped_chunks = pool.map(compute_mandel_numpy,
                              (c[i:i+chunksize,:] for i in range(0,res,chunksize)))
    pool.close()
    
    return np.vstack(escaped_chunks) / maxit

def plot_mandel(extent=[-2.0,1.0,-1.25,1.25],res=256,maxit=256,run_mandel=run_mandel_mp):
    pp.figure(figsize=(6,6))

    cmap = matplotlib.cm.coolwarm
    cmap.set_bad('k')

    pp.imshow(run_mandel(extent,res,maxit).T,extent=extent,
              cmap=cmap,norm=matplotlib.colors.PowerNorm(0.6),
              interpolation='none',origin='lower')

    pp.savefig('mandelbrot.png')
    
if __name__ == '__main__':
    plot_mandel(run_mandel=run_mandel_mp)