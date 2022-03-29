def extract_file_name(file_path):
    image = open(file_path, 'r')
    image_path = image.name.split("/")
    image_name = image_path[-1]
    return image_name