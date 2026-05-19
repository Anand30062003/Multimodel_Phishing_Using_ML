import re
import numpy as np
from PIL import Image

# ML for URL & Text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

# Deep Learning for Image
import torch
import torchvision.transforms as transforms
from torchvision import models


# ==============================
# 1. TEXT PHISHING MODEL
# ==============================
text_samples = [
    "Verify your account immediately",
    "Your account will be suspended",
    "Click here to reset your password",
    "Welcome to our official website",
    "Thank you for your registration"
]

text_labels = [1, 1, 1, 0, 0]  # 1 = Phishing, 0 = Legitimate

text_model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", SGDClassifier(loss="log_loss"))
])

text_model.fit(text_samples, text_labels)

def detect_text_phishing(text):
    probability = text_model.predict_proba([text])[0][1]
    return probability


# ==============================
# 2. URL PHISHING MODEL
# ==============================
def extract_url_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        1 if any(word in url.lower() for word in
                 ["login", "verify", "secure", "bank", "update"]) else 0
    ]

url_samples = [
    "http://secure-login-paypal.com",
    "http://verify-bank-alert.net",
    "https://www.google.com",
    "https://openai.com"
]

url_labels = [1, 1, 0, 0]

X_url = np.array([extract_url_features(url) for url in url_samples])

url_model = SGDClassifier(loss="log_loss")
url_model.fit(X_url, url_labels)

def detect_url_phishing(url):
    features = np.array(extract_url_features(url)).reshape(1, -1)
    probability = url_model.predict_proba(features)[0][1]
    return probability


# ==============================
# 3. IMAGE PHISHING MODEL
# ==============================
image_model = models.resnet18(pretrained=True)
image_model.fc = torch.nn.Linear(512, 2)  # Phishing / Legitimate
image_model.eval()

image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def detect_image_phishing(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image_transform(image).unsqueeze(0)

    with torch.no_grad():
        output = image_model(image)
        probability = torch.softmax(output, dim=1)[0][1].item()

    return probability


# ==============================
# 4. FINAL DECISION ENGINE
# ==============================
def phishing_detection(url=None, text=None, image_path=None):
    scores = []

    if url:
        url_score = detect_url_phishing(url)
        scores.append(url_score)
        print(f"URL Risk Score   : {round(url_score*100, 2)}%")

    if text:
        text_score = detect_text_phishing(text)
        scores.append(text_score)
        print(f"Text Risk Score  : {round(text_score*100, 2)}%")

    if image_path:
        image_score = detect_image_phishing(image_path)
        scores.append(image_score)
        print(f"Image Risk Score : {round(image_score*100, 2)}%")

    final_score = sum(scores) / len(scores)
    result = "PHISHING" if final_score >= 0.6 else "LEGITIMATE"

    print("-" * 40)
    print("FINAL RESULT :", result)
    print("FINAL SCORE  :", round(final_score * 100, 2), "%")

    return result, final_score


# ==============================
# 5. TEST THE SYSTEM
# ==============================
if __name__ == "__main__":
    phishing_detection(
        url="http://verify-bank-login.net",
        text="Your account will be blocked. Verify immediately",
        image_path=None   # Add image path if needed
    )
