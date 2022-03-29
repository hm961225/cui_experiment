import json
import os.path


def filename_to_url(save_position, filename: json):
    """

    :param save_position: url路径
    :param filename: 为json格式的list
    :return:
    """
    if filename:
        files = json.loads(filename)
        for i in range(len(files)):
            files[i] = os.path.join(save_position, files[i])

        return files
