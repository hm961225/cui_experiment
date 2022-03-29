import random
import string

def file_save(save_position, file):
    """

    :param save_position:
    :param file: 二进制流
    :return:
    """
    new_file_name = ''.join(random.sample(string.ascii_letters + string.digits, 20))
    with open(f"{save_position}/{new_file_name}") as f:
        f.write(file)
