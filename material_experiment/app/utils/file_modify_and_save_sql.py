import os
import json
import uuid

def file_save_to_sql(save_local_position, new_files, old_files):
    # 删除旧文件
    for file in old_files:
        # 每个file为一个属性的file列表（测试完后需加一个示例）
        if file:
            for one_file in file:
                if one_file:
                    os.remove(os.path.join(save_local_position, one_file))

    # 保存新文件
    file_list = []
    for file in new_files:
        filename = uuid.uuid1().hex
        filename += os.path.splitext(file.filename)[-1]
        # 文件存到本地
        file.save(os.path.join(save_local_position, filename))
        # 转json返回存到数据库中
        file_list.append(os.path.join(filename))
    return json.dumps(file_list)