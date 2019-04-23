import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision = 2,linewidth=10000,suppress=True)
np.random.seed(0)

COMBINERS = ["section","equal gain","max ratio"]

def BPSKRayleighDiversityBER(
    N = 2**18,                   # number of symbols
    K = 3,                        # diversity order
    Ga_l = np.logspace(-1,4,8),  # SNR values, linear scale
    combiner = "max ratio"       # one of: max ratio, section, equal gain
):
    N = N_sym # number of symbols for each simulation
    L = Ga_l.size # number of simulations
    # Indices
    n       = np.arange(N)                                        # symbol index
    l       = np.arange(L)                                        # simulation index
    k       = np.arange(K)                                        # diversity branch index
    # Sent Signal
    ss_n = (-1+0j) + 2*np.random.randint(2,size=N)
    ss_nl = np.meshgrid(ss_n,l,indexing="ij")[0]
    ss_nlk = np.meshgrid(ss_n,l,k,indexing="ij")[0]
    # Signal to Noise Ratio
    Ga_l    = np.logspace(-1,4,num=L)                                 # SNR for simulation
    Ga_nlk  = np.meshgrid(n,Ga_l,k,indexing="ij")[1]
    # Path Complex Amplitude
    al_nlk  = 1/np.sqrt(2)*(np.random.randn(N,L,K) + 1j*np.random.randn(N,L,K))
    ww_nlk  = 1/np.sqrt(2*Ga_nlk)*(np.random.randn(N,L,K) + 1j*np.random.randn(N,L,K))
    # Received Signal
    rr_nlk   = np.abs(al_nlk) * ss_nlk + ww_nlk                                # received signal with rayleigh rading and gaussian noise
    if combiner == "section":
        k_max = np.argmax(np.abs(rr_nlk),axis=2) # select branch with largest magnitude
        # Indexing magic I don't understand, credit to Stackoverflow user Divakar
        # https://stackoverflow.com/questions/42519475/python-numpy-argmax-to-max-in-multidimensional-array
        n_max,l_max = np.ogrid[:N,:L] 
        yy_nl = rr_nlk[n_max,l_max,k_max]
    elif combiner == "equal gain":
        yy_nl = np.mean(rr_nlk,axis=2)
    elif combiner == "max ratio":
        yy_nl = np.average(rr_nlk,axis=2,weights=np.abs(al_nlk)**2)
    else:
        raise Exception("Error: Combiner must be one of {}".format(COMBINERS))
    
    # Detected Symbols
    dd_nl = np.piecewise(yy_nl, [yy_nl.real < 0], [-1, 1])
    ee_nl = (dd_nl == ss_nl).astype(np.float32)
    Pe_l = 1 - np.mean(ee_nl,axis=0)

    return Pe_l



# fig, axs = plt.subplots()
# axs.plot(10*np.log10(Ga_l),Pe_l,"o-")
# axs.set_yscale("log")
