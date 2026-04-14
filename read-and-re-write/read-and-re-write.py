import h5py
import numpy as np
import soundfile as sf

# tuple holds couples of (augmentation type, augmentation metadata)
# augmenting function can return a list of those couples 

def read_file_extract_audio(h5f):
    
    word_audio = h5f['word_audio'][()]
    
    return word_audio, h5f
    
def write_aug_info(h5f, meta_tuple):
    (meta_set_name, meta_set_value) = meta_tuple
    print(f"\nmeta_set_name = {meta_set_name}\nmeta_set_value = {meta_set_value}\n")
    grp = h5f.require_group("word_augmentation_info")
    if meta_set_name in grp:
        print(f"Error with writing to h5 file!")
        return h5f
    grp.create_dataset(meta_set_name, data=meta_set_value)
    
    return h5f
    
def add_rand_noise(word_audio, h5f):
    word_audio = word_audio + 0.01*np.random.randn(*word_audio.shape)
    if "word_audio" in h5f:
        del h5f["word_audio"]
    
    h5f.create_dataset("word_audio",  data = word_audio, dtype = word_audio.dtype)
    
    return word_audio, h5f, [("random noise", "testing"), ("noise factor", 1)]
    
def debug_augmentation(h5f):
    debug_word_audio = h5f['word_audio'][()]
    sf.write("debug_word_audio.flac", debug_word_audio, 16000, format="FLAC")
    

def extract_noise_segments(noise_path):
    print(f"noise path = {noise_path}")
    with h5py.File(noise_path, "r") as f:
        
        grp = f["/data/sliced_segments"]
        fs = int(f["/meta"].attrs["sample_rate"])
        
        names = sorted(grp.keys())
        segments = [grp[n] for n in names]
        
        for segment in segments:
           end_time, start_time = segment.attrs["start_time_s"], segment.attrs["end_time_s"]
           print(f"start time = {start_time} || end time = {end_time}")
        return
    return
    
#hdf5_path = '0002_hungarian.h5'
noise_segs = extract_noise_segments(r'X:\datasets\noise_db_rotem_wav-processed-h5\26_2\harley_noise_only_boom_windmachine.h5');
# open file
#h5f = h5py.File(hdf5_path, 'r+')

# read file
#word_audio, h5f = read_file_extract_audio(h5f)

# augment and retuarn augmentation data:
#word_audio, h5f, augmentation_data = add_rand_noise(word_audio, h5f)

#print(f"\n\nword_audio = {word_audio.shape} || h5f = {h5f} || augmentation_data = {augmentation_data}\n")
# write augmentation data to file
#for aug_set in augmentation_data:
#    h5f = write_aug_info(h5f, aug_set)
    
#debug_augmentation(h5f)
# close file
#h5f.close()

print(f"\n\nDONE!\n\n")