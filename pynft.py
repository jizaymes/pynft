'''
Walks the current directory for any directories under an ./input subdirectory
Processes those images into numerical-order based images to stack images in a 
layered manner. Used to construct images of various pieces into images generated randomly

Example folder structure:
  - Current Working Directory
   |- input/
        |--- my_image_brand-edition1
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
        |---  my_image_brand-edition1
            |--- sdfs0f9sdf90sdf9sd90sf9d.png
            |--- fsf90s2k43kdfsdf23k32j4f.png
            |--- ....png

            
'''
import os
import re
import random
import sys
import uuid
import pathlib

from PIL import Image

input_path = pathlib.Path(__file__).parent + '/input/'
output_path = pathlib.Path(__file__).parent + '/output/'

parts_pattern = '^(([0-9]+)_[a-zA-Z]+)_([0-9]+)\.[pP][nN][gG]$'


#  Validate a path to see if it has the necessary files/structure to use
def make_package(file_path, foldername) -> dict:
    parts = {}  # Dictionary of parts with numeric index
    parts_w_name = {}   # Same dictionary but done with the 0_background key
    files_list = []  # List of files to carry forward to processing
    package = {}    # Package container to carry forward to processing

    folder_path = file_path + foldername + '/'

    with os.scandir(folder_path) as folders:
        for item in folders:

            if item.is_file():  # If its a file
                p_list = re.match(parts_pattern, item.name)

                if p_list:
                    # Add this to the ongoing files list
                    files_list.append(item.name)
                    # Pull apart the numerical sequence (ex. 0) of the image
                    # file name
                    part_group = p_list.group(2)
                    # Get the image part name (ex. background)
                    part_name = p_list.group(1)
                    # The sequence of the image part (ex. 1)
                    seq = p_list.group(3)

                    # If its the first time for a specific part, setup
                    # the necessary lists
                    if part_group not in parts:
                        parts[part_group] = []
                        parts_w_name[part_name] = []

                    # Add to this part / sequence to the lists
                    parts[part_group].append(seq)
                    parts_w_name[part_name].append(seq)

    # We have an background, border, and outline at minimum
    if('0' in parts and '1' in parts and '2' in parts):
        print("Cleared to move on!")
    else:
        print("Not cleared to move on. Missing Background, Border, and Body outline")
        return False

    # Make a package of all of this stuff
    package["files_list"] = files_list
    package["input_path"] = folder_path
    package["name"] = foldername  # Essentially the package name
    package["parts"] = sorted(parts)
    package["parts_w_name"] = parts_w_name

    return package


# Prepare a folder to receive the processed output. Ensures it exists, if not,
# makes it
def prepare_output_path(_output_path, _package_name):
    output_path = _output_path + _package_name

    if os.path.isdir(output_path) is False:
        print(f"Making output path : {output_path}")
        os.mkdir(output_path)


# Process an image, thereby gathering all of the necessary images, picking
# random parts, and saving it to a new composite image
def process(package, output_path) -> bool:
    print(f"Starting to process {package['name']}")

    # Temporary array so we can sort around the keys of the parts to ensure the
    # 0_ part is in proper numerical sequence
    tmp_image_parts = dict()

    # Set up and open the image for each of the parts we've located.
    for part in package['parts']:

        # Sets it to a string since the next part which re-sorts the keys
        # doesnt seem to work with a dict
        tmp_image_parts[part] = ""

    # Re-order the keys to ensure numerical sequence is followed
    # Thanks google + stackoverflow
    image_parts = {k: v for k, v in sorted(tmp_image_parts.items(), key=lambda item: item[1])}

    # Step through each part
    for part in package['parts_w_name']:

        # Send the full file_list (in package) to this function to generate the
        #  random attributes
        img = get_image_for_part(part, package)  # Key line
        # Set the image_parts dictionary with the image resource handle
        image_parts[part.split("_")[0]] = img

    # Create a new image based on the sizing of the 0_background_x file, sets
    # transparency
    output = Image.new("RGBA", image_parts['0'].size, (0, 0, 0, 0))

    # Call to make sure the directory exists, and other preparations
    prepare_output_path(output_path, package['name'])

    # Set a random file-name for our output file
    output_filename = output_path + package['name'] + '/' + uuid.uuid4().hex + '.png'

    # Step through all of the parts list
    for part in image_parts:

        # Paste the current image on top of our new output image, starting at
        # the upper left.
        output.paste(image_parts[part], (0, 0), image_parts[part])

        # Save it
        output.save(output_filename)

    print(f"All done with {package['name']} : {output_filename}")
    return True


# Receives a file list and specific part (0_background). Will pick a random
# part based on that pattern and return an image resource handle for it
def get_image_for_part(part_name, package) -> Image:
    file_list = []
    # For each file in the package
    for file in package['files_list']:

        # If it matches the part name (0_background, 3_shirt, etc)
        f_list = re.search(part_name, file)

        if f_list:  # a match
            # Add it to the list of eligible files
            file_list.append(file)

    # Pick a winner
    winner = random.choice(file_list)

    # TODO: This would be better only being done 1 time
    # Open our winner to get the size, and then crop it to remove the 1px
    # border
    tmpimg = Image.open(package['input_path'] + winner)

    # Set the height and width vars based on the size of the winning file
    h, w = tmpimg.size

    # Remove outside border by cropping. do sizing dynamically
    return tmpimg.crop((1, 1, h - 1, w - 1))


def main() -> None:
    # Iterate through the input_path for any directories
    with os.scandir(input_path) as folders:
        for item in folders:

            # If its a directory, see if its got the files we need.
            # we dont do anything with files in the input_path folder.
            #
            # TODO: Do something more detailed to validate its got all the proper image parts
            # than just checking if its a directory
            if item.is_dir():
                print(f"Item is {item}")
                # validate that there are enough parts to construct a card and
                # make a package
                package = make_package(input_path, item.name)
                if package is not False:
                    # Process this 'package' and save it in output_path
                    process(package, output_path)

                # TODO: When this is safer to run, and if there is a use_case for doing this 
                sys.exit()  # only do up to 1 directory for now


if __name__ == "__main__":
    main()
