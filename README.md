# Overview

pynft walks the any directories under the ./input subdirectory and processes 
those images into numerical-order based images to stack images in a layered manner.
Used to construct images of various pieces into images generated randomly similar to CryptoPunks 

```
Example folder structure:
  - Current Working Directory
   |- input/
        |--- my_nft_brand-edition1
            |--- 0_background_0.png
            |--- 1_border_0.png
            |--- 2_body_1.png
            |--- 2_body_2.png
            |--- 3_face_1.png
            |--- 3_face_2.png
            |--- 3_face_3.png
            |--- 4_eyes_1.png
            |--- 4_eyes_2.png
            |--- 4_eyes_3.png
            |--- 5_mouth_1.png
            |--- 5_mouth_2.png
            |--- 5_mouth_3.png
        |--- ...
    |- output/
        |---  my_nft_brand-edition1
            |--- sdfs0f9sdf90sdf9sd90sf9d.png
            |--- fsf90s2k43kdfsdf23k32j4f.png
            |--- ....png
```

# Requirements:
- Image sources made in gimp, photoshop (or similar)
- Python 3, Pillow, Rich

# How to make source files:
- Create photoshop file with many layers similar to the pynft_example.psd
- Create many layer groups with lowest number being the furthest in the background, and applied to the image first, and highest number being applied last
- Enable Generate -> Image Assets functionality and save the files in the pynft input/ folder.
- Example layer group structure
  - 4_shirtlogo
  - 3_shirt
  - 2_body
  - 1_border
  - 0_background
- Within each layer group will be the elements that can be used at random
  - 0_background
  -- 0_background_1.png
  -- 0_background_2.png
  - 1_border
  -- 1_border_0.png
  -- 1_border_1.png

  Run pynft with at minimum 0-2 positions (background, border, body) in place in the input subfolder. It will make an equivilent folder in the output path, creating an image compiling and layering all of the randomly selected images into an aggregate output file

  Image requirements:
  - Source PSD size doesnt really matter but should be +2 px in height and width to allow for a 1px border on all sides. 
  - This border will be cropped out, but is used to allow all of the images to have the same relative coordinates. 
  - Each layer item should have this 1px black border around it in a square denoting the outer bounds of the entire image set.
  - To take advantage of Photoshop's image assets generation, name each of the layers with .png so it will automatically generate the images 
  
Package Includes:
 - Example .PSD file with the layer structure I used
 - Photoshop generated image assets folder with up to >90 example images

Example output:

```
[james@Office:pynft] % python3 pynft.py
o Found: example_series1-assets
Cleared to move on!
-- Starting to process example_series1-assets
All done with example_series1-assets
output/example_series1-assets/36fead0fa92a4a30b30402e08c169b3a.png
```
