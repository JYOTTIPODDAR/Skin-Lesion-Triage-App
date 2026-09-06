import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "validator_dataset"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "skin_validator.keras"
)

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)


# ==========================================
# SETTINGS
# ==========================================

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10

SEED = 42


# ==========================================
# DATA GENERATOR
# ==========================================

train_datagen = ImageDataGenerator(

    rescale=1.0 / 255,

    validation_split=0.2,

    rotation_range=15,

    width_shift_range=0.1,

    height_shift_range=0.1,

    zoom_range=0.1,

    horizontal_flip=True
)


validation_datagen = ImageDataGenerator(

    rescale=1.0 / 255,

    validation_split=0.2
)


# ==========================================
# TRAIN DATA
# ==========================================

train_data = train_datagen.flow_from_directory(

    DATASET_PATH,

    classes=[
        "not_skin_lesion",
        "skin_lesion"
    ],

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    subset="training",

    shuffle=True,

    seed=SEED
)


# ==========================================
# VALIDATION DATA
# ==========================================

validation_data = validation_datagen.flow_from_directory(

    DATASET_PATH,

    classes=[
        "not_skin_lesion",
        "skin_lesion"
    ],

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="binary",

    subset="validation",

    shuffle=False,

    seed=SEED
)


# ==========================================
# CLASS MAPPING
# ==========================================

print("\n================================")
print("CLASS MAPPING")
print(train_data.class_indices)
print("0 = NOT SKIN LESION")
print("1 = SKIN LESION")
print("================================\n")


# ==========================================
# MODEL
# ==========================================

model = models.Sequential([

    layers.Input(
        shape=(IMG_SIZE, IMG_SIZE, 3)
    ),

    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    layers.GlobalAveragePooling2D(),

    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(0.5),

    layers.Dense(
        1,
        activation="sigmoid"
    )

])


# ==========================================
# COMPILE
# ==========================================

model.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=["accuracy"]

)


# ==========================================
# TRAIN
# ==========================================

history = model.fit(

    train_data,

    validation_data=validation_data,

    epochs=EPOCHS

)


# ==========================================
# SAVE MODEL
# ==========================================

model.save(MODEL_PATH)


print("\n================================")
print("VALIDATOR MODEL TRAINED!")
print("================================")

print("Model saved at:")

print(MODEL_PATH)

print("\nClass meaning:")

print("0 = NOT SKIN LESION")
print("1 = SKIN LESION")

print("================================")