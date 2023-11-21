from report_generator import ReportGenerator
from os import path, makedirs
from example_data_faker import fake_volumetria, fake_desmielinizantes
from pprint import pprint


def generate_reports(a, b):
    print(a)
    print(b)
    output_dir = path.join(path.dirname(__file__), "..")
    if not path.exists(output_dir):
        makedirs(output_dir)

    volumetria_report_file_path = path.join(output_dir, "reporte_volumetria.pdf")
    volumetria_report_data = fake_volumetria()
    #pprint("Saving report to %s with data:" % volumetria_report_file_path)
    #pprint(volumetria_report_data)
    ReportGenerator.generate_report(out_path=volumetria_report_file_path, report=volumetria_report_data, required_new_templates=True)

    desmielinizantes_report_file_path = path.join(output_dir, "reporte_desmielinizantes.pdf")
    desmielinizantes_report_data = fake_desmielinizantes()
    #pprint("Saving report to %s with data:" % desmielinizantes_report_file_path)
    #pprint(desmielinizantes_report_data)
    ReportGenerator.generate_report(out_path=desmielinizantes_report_file_path, report=desmielinizantes_report_data, required_new_templates=True)


if __name__ == '__main__':
    generate_reports()

