import os
import pickle
import boto3
import tempfile
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

NECESSARY_FILE_EXTENSIONS = ('csv', 'png', 'pkl')


class ReportData(object):

    def __init__(self, event, output_dir=None):

        """Base class to generate pdf reports"""
        profile_name = event['profile_name'] if 'profile_name' in event else None
        ses = boto3.Session(profile_name=profile_name)
        self.s3 = ses.client('s3')
        self.output_dir = output_dir if output_dir else tempfile.mkdtemp()
        self.bucket_name = event['bucket_name']
        self.study_prefix = event['study_prefix']
        if self.bucket_name != 'local':
            self._download_files()
        if 'findings_file' in event:
            with open(os.path.join(self.output_dir, event['findings_file']), 'rb') as f:
                self.findings = pickle.load(f)
        event['PatientName'] = event['PatientName'].rstrip('^')
        self.patient_name = event['PatientName'].replace('^', ', ').title()
        self.patient_id = event['PatientID']
        if len(self.patient_name) > 25:
            self.patient_name = self.patient_name[:7] + ' ... ' + self.patient_name[-7:]
        if len(self.patient_id) > 25:
            self.patient_id = self.patient_id[:7] + ' ... ' + self.patient_id[-7:]
        self.gender = event['PatientSex']
        self.age = event['age']
        self.title = event['title']
        self.study_name = event['StudyDescription'].title()
        if len(self.study_name) > 25:
            self.study_name = self.study_name[:7] + ' ... ' + self.study_name[-7:]
        date_string = event['StudyDate']
        self.study_date = date_string[6:8] + '/' + date_string[4:6] + '/' + date_string[:4]
        self.prev_study_name = event['prev_study_name']
        if len(self.prev_study_name) > 25:
            self.prev_study_name = self.prev_study_name[:7] + ' ... ' + self.prev_study_name[-7:]
        self.prev_study_date = event['prev_study_date']
        self.institution_logo_class = event["institution_logo_class"]
        self.send_error_pdf = event["send_error_pdf"]
        self.main = None  # To be defined by subclass
        self.event = event
        self.header = {
            'type': 'header',
            'main_img': {
                'type': 'image',
                'absolute_path': event['institution_logo'],
                'class': 'main-img'
            },
            'entelai_img': {
                'type': 'image',
                'absolute_path': os.path.join('..', 'images', 'logo-blanco.png'),
                'class': 'entelai-img'
            },
            'title': self.title,
            'table': {
                'rows': [
                    [_('Paciente'), _('ID de Paciente'), _('Nombre del estudio'), _('Fecha del estudio')],
                    [self.patient_name, self.patient_id, self.study_name, self.study_date],
                    [_('Edad'), _('Género'), _('Nombre estudio previo'), _('Fecha estudio previo')],
                    [self.age, self.gender, self.prev_study_name, self.prev_study_date],
                ]
            },
        }
        self.disclaimer = _("Producto médico autorizado por ANMAT e inscripto en el Registro Nacional de "
                            "Productores y Productos de Tecnología Médica (bajo el número 2477-1) y ANVISA "
                            "(número de registro 80102512470). Versión {}")

        self.sidebar_intro = _("Este estudio se analizó utilizando un sistema "
                                "de inteligencia artificial. Se observaron los "
                                "siguientes hallazgos para revisión por el "
                                "especialista:")
        self.error_report = {'components': [{
                                'type': 'page',
                                'class': self.institution_logo_class,
                                'components': [
                                    self.header,
                                    {'type': 'main', 'components': [
                                        {'type': 'title', 'text': _('Error al procesar el estudio')},
                                        {'type': 'paragraph', 'text': _('Se produjo un error en el procesamiento de este estudio. '
                                                                        'Por favor abra un ticket en https://soporte.entelai.com para mayor información.'
                                                                        )},
                                    ]
                                    },
                                    self.footer(1)
                                ]
                            }]}
        self.config = json.loads(event['config'])

    def footer(self, pagenum):
        footer = {
            'type': 'footer',
            'page_counter': '{}'.format(pagenum),
            'disclaimer': self.disclaimer.format(self.event['version_tag']),
        }
        return footer

    def _download_files(self, force_download=True):
        for object_name in self._get_matching_s3_keys(self.study_prefix, NECESSARY_FILE_EXTENSIONS):
            file_name = os.path.join(self.output_dir, object_name.split('/')[-1])
            if not force_download and os.path.isfile(file_name):
                continue
            self.s3.download_file(self.bucket_name, object_name, file_name)

    def _get_matching_s3_keys(self, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.

        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """
        kwargs = {'Bucket': self.bucket_name, 'Prefix': prefix}
        while True:
            resp = self.s3.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                key = obj['Key']
                if key.endswith(suffix):
                    yield key

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def upload_pdf(self):
        pdf_filename = self.event['report_file']
        pdf_path = os.path.join(self.output_dir, pdf_filename)
        response = self.s3.upload_file(pdf_path, self.bucket_name,
                                       os.path.join(self.study_prefix, pdf_filename))
