import h5py
import numpy as np

out_file = "test_h5.h5"
labels = [
    "AH",
    "T",
    "S",
    "EH",
    "N",
    "D",
    "SIL"
]

with h5py.File(out_file, 'w') as h5f:
    meta_group = h5f.create_group("metainfo")
    meta_group['Sample_Rate'] = 48000
    meta_group['SNR [dB]']    = 0
    meta_group['Labels']      = labels
    
    
print("GOODBYE!")
   
