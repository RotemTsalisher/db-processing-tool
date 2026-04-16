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
    with h5py.File(noise_path, "r") as f:
        
        grp = f["/data/sliced_segments"]
        ds = f["/data/audio"]
        
        fs = int(f["/meta"].attrs["sample_rate"])
        names = sorted(grp.keys())
        segments = [grp[n] for n in names]
        amount_of_segments = len(segments)
        
        noise_mat = np.empty(amount_of_segments, dtype=object)
        #noise_mat = [None] * amount_of_segments
        
        for (i,segment) in enumerate(segments):
           start_time, end_time = segment.attrs["start_time_s"], segment.attrs["end_time_s"]
           start_sample = int(start_time * fs)
           end_sample   = int(end_time * fs)
           noise_mat[i] = ds[start_sample:end_sample]

    return noise_mat

##############################################################################
##############################################################################
def normalize_power_db(audio: np.ndarray, target_db: float, eps: float = 1e-12, method: str = "rms"):
    log_string = f"normalize_power_db(): Hello World!"
  
    # by default will compute rms normalization
    if(method == "rms"):
        
        log_string += f"\nrms normalization, target db = {target_db}\n"
        power_linear = compute_power(audio)
        
    # unless passed with "peak" and will compute peak normalization scaling
    elif(method == "peak"):
        
        log_string += f"\npeak normalization, target db = {target_db}\n"
        power_linear = float(np.max(np.abs(audio)) + eps)
        
    # bad method arg will lead to error print and return the same audio
    else:
        
        log_string += f"\nwrong method string! RETURN WITHOUT PROCESSING!, target db = {target_db}\n"
        return audio, log_string

    target_linear = 10.0 ** (target_db / 20)
    scaler = target_linear / power_linear
    
    scaled_audio = (scaler * audio).astype(np.float32)
    return scaled_audio, log_string


def compute_power(x_, eps: float = 1e-12):
    
    pwr = float(np.sqrt(np.mean(x_**2)) + eps)
    return pwr

#def compute
def target_snr_noise_blend(x_, n_, target_snr):
    
    speech_pwr_db, noise_pwr_db = 10*np.log10(compute_power(x_)), 10*np.log10(compute_power(n_))
    snr_max = speech_pwr_db - noise_pwr_db
    
    
    return snr_max
    

def test_norm_methods(in_path: str, db: list[float], methods = ["peak", "rms", "broken"]):
    
    x, fs = sf.read(in_path)
    for method_ in methods:
        for db_ in db:
            out_path = rf"tests\norm\tests-{method_}-processed-test-speech-neg-{db_}.flac"
            y, log_string = normalize_power_db(x, db_, method = method_)
            sf.write(out_path, y, fs)
            log_string += f" saved audio || scaled {method_} to {db_} db || path = {out_path}\n\n"
            print(log_string)

    return
    
# test_norm_methods("test-speech.flac", [-3.0, -6.0, -12.0])

def test_power_computations(in_path_speech: str, in_path_noise: str):
    
    x, fs = sf.read(in_path_speech)
    x_ = normalize_power_db(x, -18)[0]
    
    noise_mat = extract_noise_segments(in_path_noise)
    
    for i in range(len(noise_mat)):
        snr_max = target_snr_noise_blend(x_, noise_mat[i], 0)
    return 
    
test_power_computations("test-speech.flac", r"./26_2/corded_extra_test.h5")
print(f"\nDONE!")