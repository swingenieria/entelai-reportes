from pdfreport.report_generator import ReportGenerator
from os import path, makedirs
from pdfreport.example_data_faker import fake_volumetria, fake_desmielinizantes, fake_quality_report, fake_study
from pprint import pprint


if __name__ == '__main__':
    output_dir = path.join(path.dirname(__file__), "")
    if not path.exists(output_dir):
        makedirs(output_dir)

    volumetria_report_file_path = path.join(output_dir, "reporte_calidad.pdf")
    volumetria_report_data = fake_study()
    pprint("Saving report to %s with data:" % volumetria_report_file_path)
    pprint(volumetria_report_data)
    ReportGenerator.generate_report(out_path=volumetria_report_file_path, report=volumetria_report_data)

