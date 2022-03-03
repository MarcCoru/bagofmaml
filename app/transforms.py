import random

import numpy as np
import torch

IGBP_simplified_classes = [
    "Forests",
    "Shrubland",
    "Savanna",
    "Grassland",
    "Wetlands",
    "Croplands",
    "Urban Build-up",
    "Snow Ice",
    "Barren",
    "Water"
]

IGBP_simplified_class_mapping = [
    0,  # Evergreen Needleleaf Forests
    0,  # Evergreen Broadleaf Forests
    0,  # Deciduous Needleleaf Forests
    0,  # Deciduous Broadleaf Forests
    0,  # Mixed Forests
    1,  # Closed (Dense) Shrublands
    1,  # Open (Sparse) Shrublands
    2,  # Woody Savannas
    2,  # Savannas
    3,  # Grasslands
    4,  # Permanent Wetlands
    5,  # Croplands
    6,  # Urban and Built-Up Lands
    5,  # Cropland Natural Vegetation Mosaics
    7,  # Permanent Snow and Ice
    8,  # Barren
    9,  # Water Bodies
]

def random_crop(img, width=32, height=32):
    x = random.randint(0, img.shape[1] - width)
    y = random.randint(0, img.shape[2] - height)
    cropxy = (y, y + height, x, x + width)
    img = img[:, cropxy[0]:cropxy[1], cropxy[2]:cropxy[3]]
    return img, cropxy


def normalize(s1, s2):
    s1 -= s1.mean(0)
    std = s1.std(0)
    std[std == 0] = 1
    s1 /= std
    s2 = s2 - s2.mean(0)
    std = s2.std(0)
    std[std == 0] = 1
    s2 /= std
    return s1, s2


def get_classification_transform(s2only):
    def transform(s1, s2, label):
        s2 = s2 * 1e-4

        if s2only:
            input = s2
        else:
            s1 = s1 * 1e-2
            input = np.vstack([s1, s2])

        igbp_label = np.bincount(label.reshape(-1)).argmax() - 1
        target = IGBP_simplified_class_mapping[igbp_label]

        if np.random.rand() < 0.5:
            input = input[:, ::-1, :]

        # horizontal flip
        if np.random.rand() < 0.5:
            input = input[:, :, ::-1]

        # rotate
        n_rotations = np.random.choice([0, 1, 2, 3])
        input = np.rot90(input, k=n_rotations, axes=(1, 2)).copy()

        if np.isnan(input).any():
            #print("found nan in input! replacing with 0")
            input = np.nan_to_num(input)
        assert not np.isnan(target).any()

        return torch.from_numpy(input), target

    return transform

