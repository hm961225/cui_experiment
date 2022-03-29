import json
import os

class CuiRemoveFiles(object):

    def cui_working_condition_remove_files(self, save_position, cui_experiment):
        """

        :param save_position: 单条cui对象
        :param cui_experiment:
        :return:
        """
        all_files = []
        if cui_experiment.experiment_facility_pic:
            experiment_facility_pic = json.loads(cui_experiment.experiment_facility_pic)
            all_files.append(experiment_facility_pic)
        if cui_experiment.sensors_distribution_pic:
            piece_pic = json.loads(cui_experiment.piece_pic)
            all_files.append(piece_pic)
        if cui_experiment.ring_pic:
            ring_pic = json.loads(cui_experiment.ring_pic)
            all_files.append(ring_pic)
        if cui_experiment.pipe_number:
            pipe_pic = json.loads(cui_experiment.pipe_pic)
            all_files.append(pipe_pic)
        if cui_experiment.sensors_distribution_pic:
            sensors_distribution_pic = json.loads(cui_experiment.sensors_distribution_pic)
            all_files.append(sensors_distribution_pic)
        if cui_experiment.sensors_distribution_table_pic:
            sensors_distribution_table_pic = json.loads(cui_experiment.sensors_distribution_table_pic)
            all_files.append(sensors_distribution_table_pic)
        if cui_experiment.working_temperature_file:
            working_temperature_file = json.loads(cui_experiment.working_temperature_file)
            all_files.append(working_temperature_file)
        if cui_experiment.ambient_relative_humidity_file:
            ambient_relative_humidity_file = json.loads(cui_experiment.ambient_relative_humidity_file)
            all_files.append(ambient_relative_humidity_file)
        self.file_remove(save_position, all_files)

    def cui_result_remove_files(self, save_position, cui_experiment):
        """

        :param cui_experiment: 单条cui对象
        :return:
        """
        all_files = []
        if cui_experiment.sensors_temperature_data_file:
            sensors_temperature_data_file = json.loads(cui_experiment.sensors_temperature_data_file)
            all_files.append(sensors_temperature_data_file)
        if cui_experiment.sensors_relative_humidity_data_file:
            sensors_relative_humidity_data_file = json.loads(cui_experiment.sensors_relative_humidity_data_file)
            all_files.append(sensors_relative_humidity_data_file)
        if cui_experiment.localized_pic:
            localized_pic = json.loads(cui_experiment.localized_pic)
            all_files.append(localized_pic)
        if cui_experiment.general_pic:
            general_pic = json.loads(cui_experiment.general_pic)
            all_files.append(general_pic)
        if cui_experiment.pitting_pic:
            pitting_pic = json.loads(cui_experiment.pitting_pic)
            all_files.append(pitting_pic)
        if cui_experiment.stress_pic:
            stress_pic = json.loads(cui_experiment.stress_pic)
            all_files.append(stress_pic)
        if cui_experiment.morphology_piece_pic:
            morphology_piece_pic = json.loads(cui_experiment.morphology_piece_pic)
            all_files.append(morphology_piece_pic)
        if cui_experiment.morphology_ring_pic:
            morphology_ring_pic = json.loads(cui_experiment.morphology_ring_pic)
            all_files.append(morphology_ring_pic)
        if cui_experiment.morphology_pipe_pic:
            morphology_pipe_pic = json.loads(cui_experiment.morphology_pipe_pic)
            all_files.append(morphology_pipe_pic)
        if cui_experiment.mass_piece_file:
            mass_piece_file = json.loads(cui_experiment.mass_piece_file)
            all_files.append(mass_piece_file)
        if cui_experiment.mass_ring_file:
            mass_ring_file = json.loads(cui_experiment.mass_ring_file)
            all_files.append(mass_ring_file)
        if cui_experiment.mass_pipe_file:
            mass_pipe_file = json.loads(cui_experiment.mass_pipe_file)
            all_files.append(mass_pipe_file)
        self.file_remove(save_position, all_files)

    @staticmethod
    def file_remove(save_position, files):
        """

        :param save_position:
        :param files: 为filename列表（数据库存的是文件的名称）
        :return:
        """
        for file in files:
            # 每个file为一个属性的file列表
            if file:
                for one_file in file:
                    if one_file:
                        os.remove(os.path.join(save_position, one_file))
