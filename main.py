from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io


app = FastAPI(
    title="Brain Tumor Classifier App"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Model Architecture
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.fc_layers = nn.Sequential(
            nn.Linear(16 * 16 * 128, 256),
            nn.ReLU(),
            nn.Linear(256, 4)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x

# Load model
model = CNN()
model.load_state_dict(
    torch.load(
        "brain_tumor_classifier.pth",
    )
)
model.eval()

# Class names
class_names = [
    "Glioma",
    "Meningioma",
    "Notumor",
    "Pituitary"
]

# Image processing
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# Prediction endpoint

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read uploaded image
    image_bytes = await file.read()

    # Convert bytes to PIL image
    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    # Apply preprocessing
    image_tensor = transform(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    # Move to device
    image_tensor = image_tensor
    # Prediction
    with torch.no_grad():

        outputs = model(image_tensor)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted_class = torch.max(
            probabilities,
            dim=1
        )

    # Get class name
    predicted_class_name = class_names[
        predicted_class.item()
    ]

    confidence_percentage = (
        confidence.item() * 100
    )

    return {
        "prediction": predicted_class_name,
        "confidence": round(
            confidence_percentage,
            2
        )
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)