import os
import shutil
from random import shuffle

# Define the root directory of your dataset
root_dir = 'student_dataset/'

# Define the subdirectories for "Good" and "Bad" images
good_dir = os.path.join(root_dir, 'Good')
bad_dir = os.path.join(root_dir, 'Bad')

# Define the target directories for "train" and "validation"
train_dir = os.path.join(root_dir, 'train')
validation_dir = os.path.join(root_dir, 'validation')

# Create the "train" and "validation" directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)

# Percentage of data to use for validation
validation_split = 0.21

# Process both "Good" and "Bad" images
for class_dir in [good_dir, bad_dir]:
    # Get a list of subdirectories (S1, S2, S3, S4)
    subdirs = [f.name for f in os.scandir(class_dir) if f.is_dir()]
    
    for subdir in subdirs:
        subdir_path = os.path.join(class_dir, subdir)
        
        # List all image files in the current subdirectory
        image_files = [f.name for f in os.scandir(subdir_path) if f.is_file()]
        
        # Shuffle the list of image files
        shuffle(image_files)
        
        # Calculate the number of images to move to the validation directory
        num_validation_samples = int(len(image_files) * validation_split)
        
        # Split the image files into training and validation sets
        train_images = image_files[num_validation_samples:]
        validation_images = image_files[:num_validation_samples]
        
        # Create the corresponding "Good" or "Bad" directories in "train" and "validation"
        train_class_dir = os.path.join(train_dir, os.path.basename(class_dir))
        validation_class_dir = os.path.join(validation_dir, os.path.basename(class_dir))
        
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(validation_class_dir, exist_ok=True)
        
        # Move images to the appropriate directories
        for image in train_images:
            src = os.path.join(subdir_path, image)
            dst = os.path.join(train_class_dir, subdir, image)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
        
        for image in validation_images:
            src = os.path.join(subdir_path, image)
            dst = os.path.join(validation_class_dir, subdir, image)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)

print("Data splitting into train and validation directories is complete.")
