import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.cluster import DBSCAN
import torch
from torchvision import transforms
import cv2

from unet import *


def count_cell_1(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применение гауссового размытия
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    # Бинаризация изображения
    #_, thresh = cv2.threshold(blurred, 180, 200, cv2.THRESH_BINARY_INV)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Нахождение контуров клеток
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Подсчет клеток
    cell_count = len(contours)
    return cell_count


def count_cell_2(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #_, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Преобразование в облако точек
    points = np.column_stack(np.where(thresh > 0))

    # Применение алгоритма кластеризации DBSCAN
    clustering = DBSCAN(eps=10, min_samples=5).fit(points)
    labels = clustering.labels_
    cell_count = len(set(labels)) - (1 if -1 in labels else 0)  # Убираем шум
    return cell_count


def count_cell_3(image):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = torch.load('models/unet_model_new.pth', weights_only=False, map_location=device)
    model.eval()  # Установите модель в режим оценки
    
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = transform(image).to(device)
    
    out = model(image.unsqueeze(0))
    out = out.cpu().squeeze(0).detach().permute(1, 2, 0).numpy()
    out = out * 255
    out = cv2.GaussianBlur(out, (11, 11), 0)
    _, out = cv2.threshold(out, 0, 255, cv2.THRESH_BINARY)
    out = out.astype(np.uint8)
    
    contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cell_count = len(contours)
    return cell_count