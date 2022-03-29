from flask import request

def acquire_files(param_name):
    """
    文件获取时如果是单个文件需要用file.get来获取，如果是多个文件则应使用file.getlist来获取
    :return:
    """
    file_obj = request.files.getlist(param_name)
    if file_obj == []:
        file_obj = request.files.get(param_name)

    return file_obj
