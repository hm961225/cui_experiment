import json

def file_modify_to_sql(file_url_list):
    filename_list = []
    for file_url in file_url_list:
        image_path = file_url.split("/")
        image_name = image_path[-1]
        filename_list.append(image_name)
    return json.dumps(filename_list)