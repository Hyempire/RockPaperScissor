import torch
from torch.utils.data import Dataset
import os
import cv2
import os.path as osp
import numpy as np
from PIL import Image
import torchvision.transforms as transforms


class RPS_Dataset(Dataset):
    def __init__(self, data_dir, split):
        self.data_dir = data_dir
        self.transform = transforms.ToTensor()
        self.split = split
        if self.split == "train":
            self.img_path_list = os.listdir(data_dir)[
                : int(len(os.listdir(data_dir)) * 0.8)
            ]
        elif self.split == "valid":
            self.img_path_list = os.listdir(data_dir)[
                int(len(os.listdir(data_dir)) * 0.8) : int(
                    len(os.listdir(data_dir)) * 0.9
                )
            ]
        else:
            self.img_path_list = os.listdir(data_dir)[
                int(len(os.listdir(data_dir)) * 0.9) :
            ]

    def __len__(self):
        return len(self.img_path_list)

    def __getitem__(self, idx):
        filename = self.img_path_list[idx]
        filepath = osp.join(self.data_dir, filename)
        img = Image.open(filepath)
        img = self.transform(img)
        label_check = filename.split("_")[0]
        if label_check == "paper":
            label = 0
        elif label_check == "rock":
            label = 1
        else:
            label = 2
        return img, label
