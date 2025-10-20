import os
import re

# Input and output folder paths
input_folder = "../frontend/static/css"  # your original CSS folder
output_folder = "../frontend/static/minified-css"  # folder to save minified files

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)


def minify_css(css_content):
  # Remove comments
  css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.S)
  # Remove whitespace and newlines
  css_content = re.sub(r'\s+', ' ', css_content)
  # Remove spaces around symbols
  css_content = re.sub(r'\s*([{};:>,])\s*', r'\1', css_content)
  return css_content.strip()


# Loop through files in input folder
overall_difference = 0
total_input_size = 0
total_output_size = 0
for filename in os.listdir(input_folder):
  if filename.endswith(".css"):
    input_path = os.path.join(input_folder, filename)
    input_filesize = os.path.getsize(input_path) / 1024
    total_input_size += input_filesize

    with open(input_path, "r", encoding="utf-8") as f:
      css_content = f.read()

    minified = minify_css(css_content)

    # Add suffix before extension
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}-min{ext}"
    output_path = os.path.join(output_folder, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
      f.write(minified)

    print(f"Minified: {filename} -> {output_filename}")
    filesize = os.path.getsize(output_path) / 1024
    total_output_size += filesize

overall_difference = total_input_size - total_output_size
print("Before compression: ", total_input_size, "kb")
print("After compression: ", total_output_size, "kb")
print("compression: ", overall_difference, "kb")
