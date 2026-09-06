import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os


# ==============================
# SETTINGS
# ==============================

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10

DATASET_PATH = "dataset"
MODEL_PATH = "models/skin_lesion_model.keras"


# ==============================
# DATA PREPROCESSING
# ==============================

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)


train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)


validation_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)


# ==============================
# LOAD MOBILENETV2
# ==============================

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)


# Freeze pretrained layers
base_model.trainable = False


# ==============================
# BUILD MODEL
# ==============================

x = base_model.output

x = GlobalAveragePooling2D()(x)

x = Dense(256, activation="relu")(x)

x = Dropout(0.3)(x)

output = Dense(
    train_data.num_classes,
    activation="softmax"
)(x)


model = Model(
    inputs=base_model.input,
    outputs=output
)


# ==============================
# COMPILE MODEL
# ==============================

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# ==============================
# TRAIN MODEL
# ==============================

print("\nStarting Model Training...\n")

history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=EPOCHS
)


# ==============================
# SAVE MODEL
# ==============================

os.makedirs("models", exist_ok=True)

model.save(MODEL_PATH)

print("\nModel Training Completed! 🎉")

print(f"Model saved at: {MODEL_PATH}")


# ==============================
# SHOW CLASSES
# ==============================

print("\nDetected Classes:")

print(train_data.class_indices)