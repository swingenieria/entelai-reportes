import json
import logging
import traceback
from .helpers.language import set_language
from .report_generator import ReportGenerator
from os import path, makedirs
from .report_data.neuro_report_data import VolumetriaReportData, DesmielinizantesReportData
from .report_data.thorax_report_data import ThoraxReportData, CovidThoraxReportData
from .report_data.mammo_report_data import MammoReportData

logger = logging.getLogger()
logger.setLevel(logging.INFO)


report_mapping = {"VolumetriasPipeline": VolumetriaReportData,
                  "VolumetriasPipelineLong": VolumetriaReportData,
                  "EsclerosisMultipleSinGadoPipeline": DesmielinizantesReportData,
                  "EsclerosisMultipleSinGadoPipelineLong": DesmielinizantesReportData,
                  "EsclerosisMultiplePipelineLong": DesmielinizantesReportData,
                  "EsclerosisMultiplePipeline": DesmielinizantesReportData,
                  "ThoraxPipeline": ThoraxReportData,
                  "CovidThoraxPipeline": CovidThoraxReportData,
                  "MammoPipeline": MammoReportData,
                  }

required_new_templates = {
    "VolumetriasPipeline": True,
    "VolumetriasPipelineLong": True,
    "EsclerosisMultipleSinGadoPipeline": True,
    "EsclerosisMultipleSinGadoPipelineLong": True,
    "EsclerosisMultiplePipelineLong": True,
    "EsclerosisMultiplePipeline": True,
    "ThoraxPipeline": False,
    "CovidThoraxPipeline": False,
    "MammoPipeline": False,
}

def generate_reports(event, context):

    language = event.get('language', 'es_AR')
    logger.info(f'SETTING LANGUAGE AS {language}')
    set_language(language)

    if event['bucket_name'] == 'local':
        output_dir = event['study_prefix']
    else:
        output_dir = "/tmp/entelai-tmp"
    makedirs(output_dir, exist_ok=True)
    report_file_path = path.join(output_dir, event['report_file'])
    logger.info(f"Starting report generation for {event['study_prefix']}")
    try:
        report_type = report_mapping[event['report_type']]
        report_data_generator = report_type(event, output_dir)
        report_data = report_data_generator.get_report_data()
        new_templates = required_new_templates[event['report_type']]
        ReportGenerator.generate_report(out_path=report_file_path, report=report_data, required_new_templates=new_templates)
        if event['bucket_name'] != 'local':
            report_data_generator.upload_pdf()
    except Exception as e:
        logger.error("Error in report generation", exc_info=True)
        desc = traceback.format_exc()
        return {'Status': 'Error', 'Exception': desc}
    return {'Status': 'Success'}


if __name__ == '__main__':
    with open('../event_thorax.json') as f:
        event = json.load(f)
    generate_reports(event=event, context=None)
