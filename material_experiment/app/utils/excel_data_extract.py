import os.path
import json
import xlrd


def parse_excel(save_position, file_name):
    """
    解析excel文件
    """
    if file_name:
        file_name = json.loads(file_name)
        if file_name != []:
            string_file_name = file_name[0]
            file_path = os.path.join(save_position, string_file_name)
            file = xlrd.open_workbook(file_path)
            table = file.sheets()[0]
            all_rows = table.nrows
            return table, all_rows
        else:
            return [], []
    return [], []

def extract_all_data(save_postiton, file_name):
    """
    获取表格的全部数据
    """
    all_data = []
    table, all_rows = parse_excel(save_postiton, file_name)
    if table != []:
        for row in range(all_rows):
            if row == 0:
                continue
            all_data.append(table.row_values(row))
        return all_data

def extract_x_y_data(save_position, file_name):
    """
    解析excel文件，返回文件中的数据
    :param file_obj:
    :return: data: 坐标二维数组
    """
    data = []
    table, all_rows = parse_excel(save_position, file_name)
    if table != []:
        for row in range(all_rows):
            # 取第一列为x轴数据，第4列为y轴数据
            if row == 0:
                continue
            x = table.row_values(row, start_colx=0, end_colx=1)
            y = table.row_values(row, start_colx=2, end_colx=3)
            # row_values返回的是一个列表，所以需要取列表中的元素来赋值
            data.append([x[0], y[0]])

        return data

def extract_x_y_z_data(save_position, file_name):
    data = []
    table, all_rows = parse_excel(save_position, file_name)
    if table != []:
        for row in range(all_rows):
            if row == 0:
                continue
            num = table.row_values(row, start_colx=0, end_colx=1)
            x = table.row_values(row, start_colx=1, end_colx=2)
            y = table.row_values(row, start_colx=2, end_colx=3)
            z = table.row_values(row, start_colx=3, end_colx=4)
            one_data = {
                "sensor": num[0],
                "xp": x[0],
                "yp": y[0],
                "zp": z[0]
            }
            data.append(one_data)

        return data

def extract_data_from_name(save_position, file_name, *args):
    # cow_number 为excel的列数
    data_name_list = []
    for data_name in args:
        data_name_list.append(data_name)

    data = []
    table, rows_count = parse_excel(save_position, file_name)
    if table != []:
        need_col = []
        cols_count = table.ncols
        for row in range(rows_count):
            if row == 0:
                # 记录之后需要提取的列号
                for col in range(cols_count):
                    # table.row_values(row, start_colx=col, end_colx=col+1)[0]结果是个list取第一个元素即可
                    if table.row_values(row, start_colx=col, end_colx=col+1)[0] in data_name_list:
                        need_col.append(col)
            else:
                one_row_data = []
                for col in need_col:
                    one_row_data.append(table.row_values(row, start_colx=col, end_colx=col+1)[0])

                data.append(one_row_data)

    return data



def extract_x_y_data_to_three_array(save_position, file_name):
    """
    解析excel文件，返回文件中的数据
    :param file_obj:
    :return: data: 坐标三维数组
    """
    # 总体思路：就是调用extract_x_y函数来取特定的列，本函数只需要将结果添加到一个新的数组中即可
    pass

def extract_mass_piece_data(save_position, file_name):
    """
    解析excel文件：返回文件中的数据
    """
    data = []
    table, all_rows = parse_excel(save_position, file_name)
    if table != []:
        for row in range(all_rows):
            if row == 0:
                continue
            num = table.row_values(row, start_colx=0, end_colx=1)
            before = table.row_values(row, start_colx=1, end_colx=2)
            after = table.row_values(row, start_colx=2, end_colx=3)
            delta = table.row_values(row, start_colx=3, end_colx=4)
            corrosion_rate = table.row_values(row, start_colx=4, end_colx=5)
            one_data = {
                "number": num[0],
                "before": before[0],
                "after": after[0],
                "delta": delta[0],
                "corrosion_rate": corrosion_rate[0],
            }
            data.append(one_data)

        return data

def extract_data_without_name(save_position, file_name):
    data = []
    table, all_rows = parse_excel(save_position, file_name)
    if table != []:
        all_cols = table.ncols
        for col in range(all_cols):
            if col == 0 or col == 1:
                continue
            one_col_data = []
            for row in range(all_rows):
                if row == 0:
                    continue
                one_data_list = []
                one_data = table.col_values(col, start_rowx=row, end_rowx=row+1)
                one_data_list.append(row)
                one_data_list.append(one_data[0])

                one_col_data.append(one_data_list)
            data.append(one_col_data)
        return data

def extract_ambient_data(save_position, file_name):
    data = []
    table, all_rows = parse_excel(save_position, file_name)
    if table != []:
        one_line_data = []
        other_line_data = []
        for row in range(all_rows):
            if row == 0:
                continue
            num = table.row_values(row, start_colx=0, end_colx=1)
            x = table.row_values(row, start_colx=1, end_colx=2)
            y = table.row_values(row, start_colx=2, end_colx=3)
            one_line_data.append([num[0], x[0]])
            other_line_data.append([num[0], y[0]])
        data.append(one_line_data)
        data.append(other_line_data)

        return data

def extract_sensors_data(save_position, file_name):
    data = []
    table, all_rows = parse_excel(save_position, file_name)
    if table != []:
        temperature_list = []
        humidity_list = []
        all_cols = table.ncols
        for col in range(all_cols):
            if col == 0 or col == 1:
                continue
            if col % 2 != 0:
                one_col_data = []
                for row in range(all_rows):
                    if row != 1:
                        if row == 0 or row % 3600 != 0:
                            continue
                    one_data_list = []
                    one_data = table.col_values(col, start_rowx=row, end_rowx=row+1)
                    one_data_list.append(row)
                    one_data_list.append(one_data[0])
                    one_col_data.append(one_data_list)
                temperature_list.append(one_col_data)
            else:
                one_col_data = []
                for row in range(all_rows):
                    if row == 0:
                        continue
                    one_data_list = []
                    one_data = table.col_values(col, start_rowx=row, end_rowx=row+1)
                    one_data_list.append(row)
                    one_data_list.append(one_data[0])
                    one_col_data.append(one_data_list)
                humidity_list.append(one_col_data)

        data.append(temperature_list)
        data.append(humidity_list)
        return data
