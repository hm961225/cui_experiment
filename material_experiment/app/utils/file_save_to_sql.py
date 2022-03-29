import os
import json
import uuid

def file_save_to_sql(save_local_position, files):

    file_list = []
    if files != None and files != []:
        for file in files:
            filename = uuid.uuid1().hex
            filename += os.path.splitext(file.filename)[-1]
            # 文件存到本地
            file.save(os.path.join(save_local_position, filename))
            # 转json返回存到数据库中
            file_list.append(os.path.join(filename))
    return json.dumps(file_list)