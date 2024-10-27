# Advice: good practic to comment what library do and why we need it.
# also, according to coding standart, a program must have a documentation. ;)

"""What is this?

What this program do?
"""

# What is it?
import numpy as np # For what we use it?

# What is it?
import cv2 # For what we use it?

# What is it?
from tqdm import tqdm # For what we use it?

# What is it?
from scipy import ndimage # For what we use it?

# What is it? 
from skimage import img_as_ubyte # For what we use it?
from skimage import img_as_float # For what we use it?
from skimage.color import rgb2gray # For what we use it?
from skimage import restoration # For what we use it?

# What is "restoration"? 
from skimage.restoration import denoise_nl_means # For what we use it?
from skimage.restoration import estimate_sigma # For what we use it?
from skimage.restoration import denoise_wavelet # For what we use it?


# The types for function and parametrs improve readability
# and understanding of program.

## The next advice: see, you use in (anchor 1) code, that works with files. 
## And we can see, that this code repeats in all functions, that use methods to
## convert images. Can we create a function, that will have cycle for all images
## and convert this images from the conver_params? See, i means we don't need functions
## for convertation, because the library already realized it. It's good idea to create
## function, as i already said, that only choose suitable method for convertation.
## This advice concerns all your converts functions :) 
def wiener(files, progress_bar, progress_label, root): 
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    # It's no good idea use magical numbers
    psf = np.ones((5, 5)) / 25
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_float(rgb2gray(files[i]))
        restored_img, _ = restoration.unsupervised_wiener(img, psf) # anchor 1
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img))
            / (np.max(restored_img) - np.min(restored_img))
        )
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
        #==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def gauss(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    # nit: dont ise i in cycles. It's more beautiful, if you use, for example
    # file_index. Because, if you have a nested cycle, you can forget, what i and, 
    # e.g. "j" means.
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        restored_img = ndimage.gaussian_filter(files[i], 2)
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def median(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    # init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        restored_img = ndimage.median_filter(files[i], 3)
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def contrast(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        restored_img = clahe.apply(files[i])
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def sharpen(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    # It's no good idea use magical numbers
    sharpen_mask = np.array([
                    [ -1, -1, -1 ],
                    [ -1,  9, -1 ],
                    [ -1, -1, -1 ], # nit: good idea to put comma in 
                                    # the end of the list
                ])
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        restored_img = cv2.filter2D(files[i], -1, sharpen_mask)
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def denoise(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    patch_kw = dict(patch_size=2, patch_distance=2)
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        sigma_est = np.mean(estimate_sigma(files[i]))
        img = img_as_float(files[i])
        restored_img = denoise_nl_means(
            img,
            h=0.8 * sigma_est,
            sigma=sigma_est,
            fast_mode=False,
            **patch_kw,
        )
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img))
            / (np.max(restored_img) - np.min(restored_img))
        )
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def deconvolution(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    psf = np.ones((3, 3)) / 25
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_float(rgb2gray(files[i]))
        restored_img = restoration.richardson_lucy(img, psf)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img))
            / (np.max(restored_img) - np.min(restored_img))
        )
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def wavelet(files, progress_bar, progress_label, root):
    """Functions need a information about what they do"""
    
    # This is a good idea to take this code in the function, for example 
    #init_progress_bar(), because this code uses in program > 2 time
    progress_step = 100 / len(files)
    progress_bar["value"] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    #========

    result_array = []
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_float(rgb2gray(files[i]))
        restored_img = denoise_wavelet(img, rescale_sigma=True)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img))
            / (np.max(restored_img) - np.min(restored_img))
        )
        result_array.append(restored_img)
        # It's good idea to take this part of code in function too. For my opinion
        # good name for this function upate_progress_bar(params...). Dont forget
        # to use types :)
        progress_bar["value"] += progress_step
        progress_label.config(text=round(progress_bar["value"]))
        root.update_idletasks()
        # ==========
    # also in function (update_progress_bar(params...). In those function check
    # the condition progress_bar += step > 100. You can put in the while e.g.
    progress_bar["value"] = 100
    progress_label.config(text=progress_bar["value"])
    root.update_idletasks()   
    #==========
    return result_array



# The types for function and parametrs improve readability
# and understanding of program.
def filtration_gui_main(files, mode, progress_bar_info):
    """Functions need a information about what they do"""

    result_array = []
    if mode == "Без предобработки":
        result_array = files
    if mode == "Винер":
        result_array = wiener(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Гаусс":
        result_array = gauss(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Медианный":
        result_array = median(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Контраст":
        result_array = contrast(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Резкость":
        result_array = sharpen(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Шумоподавление":
        result_array = denoise(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Обратная свёртка":
        result_array = deconvolution(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    if mode == "Вейвлет":
        result_array = wavelet(
            files,
            progress_bar_info[0],
            progress_bar_info[1],
            progress_bar_info[2],
        )
    return result_array


