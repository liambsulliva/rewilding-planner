from PIL import Image
import numpy as np
from scipy.ndimage import label, distance_transform_edt, center_of_mass
from skimage.feature import peak_local_max
import torch
import torch.nn.functional as F
from torchvision.utils import save_image

def score_map(raster):
    # Parse array and count unique items
    for key, value in pixeldict_tensors.items():
        # Find where pixel values match the dictionary value
        match = torch.all(raster == value, dim=-1)
    
        # Update the pixel count
        pixelcount[key] += match.sum().item()

    # Print the pixel counts
    print(pixelcount)

    total = sum(pixelcount.values())
    water_diff = abs((1/6)-pixelcount['water']/total)
    shaded_diff = abs((1/6)-pixelcount['shaded']/total)
    open_diff = abs((2/3)-pixelcount['open']/total)
    print("water diff " + str(water_diff))
    print("shaded diff " + str(shaded_diff))
    print("open " + str(open_diff))

    biodiversity_score = 1 - (sum([water_diff, shaded_diff, open_diff]) / 3)
    bush_count = (biodiversity_score-.2)*pixelcount['open']
    carbon_count = (pixelcount['shaded']*9.4)/1000
    bush_carbon_count = (bush_count*8.3)/1000

    print(carbon_count)
    print(biodiversity_score)
    print(bush_count)
    print(bush_carbon_count)

def remove_tree(treenum, stumpraster, leafraster):
    for i, row in enumerate(stumpraster):
        for j, element in enumerate(row):
            if element==treenum or leafraster[i][j]==treenum:
                pixels[i][j] = torch.tensor([42,242,12], dtype=torch.int32)


def find_nearest_centroid(location, centroids):
    nearest_stump = 0
    nearest_distance = 100000000
    
    for i, cs in enumerate(centroids):
        dist = torch.sqrt(torch.sum((location - cs) ** 2))
        if  dist < nearest_distance:
            nearest_stump = i+1
            nearest_distance = dist

    return nearest_stump


def make_leafmap(tree_stumps, leaves):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tree_stumps = tree_stumps.to(device)
    leaves = leaves.to(device)

    # Step 1: Label individual stumps (on CPU as scipy doesn't support GPU)
    tree_stumps_np = tree_stumps.cpu().numpy()
    labeled_stumps, num_stumps = label(tree_stumps_np)
    np.savetxt('stumps', labeled_stumps, delimiter=',')
    # Step 2: Calculate centroids for each stump (on CPU)
    stump_centroids = center_of_mass(tree_stumps_np, labels=labeled_stumps, index=range(1, num_stumps+1))
    stump_centroids_pixels = [torch.tensor([int(round(y)), int(round(x))]) for y, x in stump_centroids]

    # Step 3: Parse leaf_grid
    for i, row in enumerate(leaves):
        for j, element in enumerate(row):
            if element==1:
                leaves[i][j] = find_nearest_centroid(torch.tensor([i,j]), stump_centroids_pixels)

    np.savetxt('tensor.txt', leaves, delimiter=',') 

    return(labeled_stumps, leaves)
    # # Step 5: Find leaf locations using GPU
    # leaf_locations = torch_peak_local_max(leaves)
    # leaf_locations_pixels = [(int(y), int(x)) for y, x in leaf_locations.cpu().numpy()]


    # # Step 6: For each leaf, find the nearest tree stump
    # #leaf_distances = distance[leaf_locations[:, 0], leaf_locations[:, 1]]
    # nearest_stump_indices = centroid_tensor[leaf_locations[:, 0], leaf_locations[:, 1]]
    
    # # Create a list of tuples (leaf_location, nearest_stump_centroid)
    # nearest_stumps = [
    #     (leaf.cpu().numpy(), stump_centroids[int(stump_idx) - 1])
    #     for leaf, stump_idx in zip(leaf_locations, nearest_stump_indices)
    #     if stump_idx > 0  # Ensure we have a valid stump index
    # ]
    
    # return nearest_stumps, stump_centroids_pixels, leaf_locations_pixels


file = "ugh.bmp"
img = Image.open(file)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pixels = torch.tensor(np.array(img), dtype=torch.int32)

pixeldict = {'water':[1, 1, 255],'stump':[169,46,47], 'bush':[255,1,1],'shaded':[10,152,20],'open':[42,242,12]}
pixelcount = {'water':0,'stump':0, 'bush':0,'shaded':0,'open':0}

stumpraster = torch.zeros(pixels.shape[:-1], dtype=torch.int32)  # Only 2D since it's a mask (no RGB channels)
leafraster = torch.zeros(pixels.shape[:-1], dtype=torch.int32)
pixels = pixels.to(device)
stumpraster = stumpraster.to(device)
leafraster = leafraster.to(device)

pixeldict_tensors = {key: torch.tensor(value, dtype=torch.int32) for key, value in pixeldict.items()}

score_map(pixels)
 
stumpraster = torch.where(torch.all(pixels == pixeldict_tensors['stump'], dim=-1), 1, stumpraster)
leafraster = torch.where(torch.all(pixels == pixeldict_tensors['shaded'], dim=-1), 1, leafraster)
np.savetxt('tensor.txt', leafraster, delimiter=',') 

stumpraster, leafraster =make_leafmap(stumpraster, leafraster)

remove_tree(3, stumpraster, leafraster)
pixel_np = pixels.cpu().numpy().astype(np.uint8)
im = Image.fromarray(pixel_np)
im.save("2.bmp")
