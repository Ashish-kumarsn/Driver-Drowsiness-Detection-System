import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix

# ================= CONFIG =================

IMG_SIZE = 24
TRAIN_DIR = "train"     # train/closed , train/open
TEST_DIR  = "test"      # test/Closed , test/Open
MODEL_PATH = "eye_cnn_model.h5"
LABELS = ["Closed", "Open"]

# ================= LOAD DATA FUNCTION =================

def load_data(base_dir, categories):
    data = []
    labels = []

    for label, folder_name in enumerate(categories):
        folder_path = os.path.join(base_dir, folder_name)
        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            data.append(img)
            labels.append(label)

    data = np.array(data).reshape(-1, IMG_SIZE, IMG_SIZE, 1) / 255.0
    labels = to_categorical(labels, 2)
    return data, labels

# ================= LOAD DATA =================

# Train data (lowercase folders)
X_train, y_train = load_data(TRAIN_DIR, ["closed", "open"])

# Test data (capital folders)
X_test, y_test = load_data(TEST_DIR, ["Closed", "Open"])

print("Train samples:", X_train.shape[0])
print("Test samples :", X_test.shape[0])

# ================= LOAD MODEL =================

model = load_model(MODEL_PATH)
print("✅ Model loaded successfully")

# =================================================
# 1️⃣ CONFUSION MATRIX (NO RETRAINING)
# =================================================

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

cm = confusion_matrix(y_true, y_pred_classes)

plt.figure(figsize=(5,4))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=LABELS,
    yticklabels=LABELS
)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# =================================================
# 2️⃣ & 3️⃣ ACCURACY + LOSS (RETRAIN 5 EPOCHS)
# =================================================

history = model.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)

# -------- Accuracy --------
plt.figure(figsize=(6,4))
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Epochs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("accuracy_vs_epochs.png")
plt.show()

# -------- Loss --------
plt.figure(figsize=(6,4))
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Loss vs Epochs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("loss_vs_epochs.png")
plt.show()
