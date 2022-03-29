import uuid
import os
from app.utils.file_save_to_sql import file_save_to_sql

def file_save(save_local_position, files):
    """

    :param save_position:
    :param files: 列表形式的json字符串（包含若干张图片）
    :return:
    """
   # filename = uuid.uuid1().hex
    for file in files:
        file.save(os.path.join(save_local_position, file.filename))
        # file_save_to_sql(os.path.join(save_position, filename))
