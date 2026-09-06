import os
import numpy as np
from PIL import Image
import tensorflow as tf


# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAVE_PATH = os.path.join(
    BASE_DIR,
    "validator_dataset",
    "not_skin_lesion"
)

os.makedirs(SAVE_PATH, exist_ok=True)


# ==========================================
# DOWNLOAD CIFAR-10 DATASET
# ==========================================

print("Downloading CIFAR-10 dataset...")

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()


# ==========================================
# COMBINE DATA
# ==========================================

images = np.concatenate(
    [x_train, x_test],
    axis=0
)


# ==========================================
# NUMBER OF IMAGES
# ==========================================

NUM_IMAGES = 2000


# ==========================================
# SAVE RANDOM IMAGES
# ==========================================

print(f"\nSaving {NUM_IMAGES} images...")

for i in range(NUM_IMAGES):

    image = Image.fromarray(images[i])

    file_path = os.path.join(
        SAVE_PATH,
        f"not_skin_{i}.jpg"
    )

    image.save(file_path)


print("\n====================================")
print("DONE!")
print(f"{NUM_IMAGES} images saved successfully.")
print("Location:")
print(SAVE_PATH)
print("====================================")