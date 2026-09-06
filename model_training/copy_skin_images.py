import os
import shutil

# Current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Existing dataset
SOURCE_DIR = os.path.join(BASE_DIR, "dataset")

# Validator dataset
DESTINATION_DIR = os.path.join(
    BASE_DIR,
    "validator_dataset",
    "skin_lesion"
)

# Create destination folder if needed
os.makedirs(DESTINATION_DIR, exist_ok=True)


# Skin lesion class folders
CLASSES = [
    "AK",
    "BCC",
    "BKL",
    "DF",
    "MEL",
    "NV",
    "SCC",
    "VASC"
]


count = 0

for class_name in CLASSES:

    class_path = os.path.join(SOURCE_DIR, class_name)

    if not os.path.exists(class_path):
        print(f"Folder not found: {class_name}")
        continue

    for filename in os.listdir(class_path):

        source_file = os.path.join(class_path, filename)

        # Skip folders
        if not os.path.isfile(source_file):
            continue

        # Add class name to avoid duplicate filenames
        destination_file = os.path.join(
            DESTINATION_DIR,
            f"{class_name}_{filename}"
        )

        shutil.copy2(source_file, destination_file)

        count += 1


print("\n==============================")
print(f"Successfully copied {count} images!")
print("==============================")