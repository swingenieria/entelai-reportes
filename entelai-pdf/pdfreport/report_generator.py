from jinja2 import Environment, PackageLoader
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
import sys
import logging
import os

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)  # Change logging level accordingly

REPORT_SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_FOLDER_PATH = os.path.join(REPORT_SCRIPT_FOLDER, "templates")
TEMPLATES_FOLDER_PATH2 = os.path.join(REPORT_SCRIPT_FOLDER, "templates_2023")
MAIN_TEMPLATE_PATH = os.path.join(TEMPLATES_FOLDER_PATH, "index.html")
MAIN_TEMPLATE_PATH2 = os.path.join(TEMPLATES_FOLDER_PATH2, "index.html")

FONT_CONFIG = FontConfiguration()

with open(MAIN_TEMPLATE_PATH, 'r') as file_obj:
    RENDERER = Environment(loader=PackageLoader("templates", ".")).from_string(file_obj.read())

with open(MAIN_TEMPLATE_PATH2, 'r') as file_obj:
    RENDERER2 = Environment(loader=PackageLoader("templates_2023", ".")).from_string(file_obj.read())

def url_for(role, filename):
    return filename


def load_img(absolute_file_path):
    return absolute_file_path


KWARGS = {
    'url_for': url_for,
    'load_img': load_img,
    'body_class': ''
}

class ReportGenerator:
    @staticmethod
    def generate_report(out_path, report, required_new_templates=False):
        if required_new_templates:
            html_string = RENDERER2.render({'report': report}, **KWARGS)
            html = HTML(base_url=TEMPLATES_FOLDER_PATH2, string=html_string)
            html.write_pdf(out_path, font_config=FONT_CONFIG)
        else:
            html = HTML(base_url=TEMPLATES_FOLDER_PATH, string=RENDERER.render({'report': report}, **KWARGS))
            html.write_pdf(out_path, font_config=FONT_CONFIG)
        return out_path
