import numpy as np
from scipy.ndimage import binary_dilation


def feather(foreg, backg, overlap, foreg_valid, radius=4):
    coeffs = [1.0 - float(x)/(radius + 1) for x in range(1, radius + 1)]

    dilated = ~foreg_valid
    prev = np.zeros(foreg_valid.shape, dtype=bool)
    for bgcoeff in coeffs:
        dilated = binary_dilation(dilated) & overlap
        fmask = dilated ^ prev
        prev = dilated

        fgcoeff = 1.0 - bgcoeff
        foreg[fmask] = (fgcoeff * foreg[fmask] +
                        bgcoeff * backg[fmask])
    
    return foreg