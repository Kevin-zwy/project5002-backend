# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import torch
import torchvision.models as models
import torch
from PIL import Image
from torchvision import transforms

class CustomResNet50(nn.Module):
    def __init__(self, num_classes):
        super(CustomResNet50, self).__init__()
        # load ResNet50
        self.base_model = models.resnet50(weights='IMAGENET1K_V1')


        self.base_model.fc = nn.Identity()


        self.fc1 = nn.Linear(2048, 512)
        self.fc2 = nn.Linear(512, num_classes)


        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.base_model(x)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x



class CustomDenseNet121(nn.Module):
    def __init__(self, num_classes):
        super(CustomDenseNet121, self).__init__()
        # load DenseNet121
        self.base_model = models.densenet121(weights='IMAGENET1K_V1')

        # Remove the classification layer
        self.base_model.classifier = nn.Identity()

        self.fc1 = nn.Linear(1024, 512)
        self.fc2 = nn.Linear(512, num_classes)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.base_model(x)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class CustomMobileNetV2(nn.Module):
    def __init__(self, num_classes):
        super(CustomMobileNetV2, self).__init__()
        # load MobileNetV2
        self.base_model = models.mobilenet_v2(weights='IMAGENET1K_V1')


        self.base_model.classifier = nn.Identity()


        self.fc1 = nn.Linear(1280, 512)
        self.fc2 = nn.Linear(512, num_classes)


        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.base_model(x)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x





def predict_image_voting(image_path, models, device, class_names):

    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = transform(image).unsqueeze(0).to(device)


    predictions = []

    for model in models:
        model.to(device)
        model.eval()

        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)
            predictions.append(predicted.item())


    final_prediction = max(set(predictions), key=predictions.count)


    predicted_class_name = class_names[final_prediction]

    return predicted_class_name


def main():
    # Load the models
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    class_names = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 'Atopic Dermatitis Photos', 'Bullous Disease Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Hair Loss Photos Alopecia and other Hair Diseases', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Nail Fungus and other Nail Disease', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Scabies Lyme Disease and other Infestations and Bites', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']
    num_classes = 23
    model_resnet = CustomResNet50(num_classes=num_classes).to(device)
    model_densenet = CustomDenseNet121(num_classes=num_classes).to(device)
    model_mobilenetv2 = CustomMobileNetV2(num_classes=num_classes).to(device)

    # model_resnet = CustomResNet50(num_classes=num_classes)

    loaded_model_resnet = torch.load(r'../detection/resnet50_skin_disease_model.pth', weights_only=False, map_location=device)
    loaded_model_densenet = torch.load(r'../detection/DenseNet121_skin_disease_model_29.pth', weights_only=False, map_location=device)
    loaded_model_mobilenetv2 = torch.load(r'../detection/mobilenet__skin_disease_model.pth', weights_only=False, map_location=device)
    # Check if the loaded file is a dictionary (state_dict) or the model itself
    if isinstance(loaded_model_resnet, dict):
        model_resnet.load_state_dict(loaded_model_resnet)
        model_densenet.load_state_dict(loaded_model_densenet)
        model_mobilenetv2.load_state_dict(loaded_model_mobilenetv2)
    else:
        # If it's the model, assign it directly
        model_resnet = loaded_model_resnet
        model_densenet = loaded_model_densenet
        loaded_model_mobilenetv2 = loaded_model_mobilenetv2

    model_resnet.to(device)
    model_densenet.to(device)
    loaded_model_mobilenetv2.to(device)

    models=[model_resnet,model_densenet,model_mobilenetv2]


if __name__ == '__main__':
    main()