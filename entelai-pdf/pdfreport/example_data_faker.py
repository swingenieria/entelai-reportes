from faker import Faker
import random
from os import path

fake = Faker("es_MX")
dirname = path.dirname(path.abspath(__file__))


def fake_quality_report():
    output_dir = '/home/fran/repos/entelai-quality-report/pruebas'
    header = {
        'type': 'header',
        'main_img': {
            'type': 'image',
            'absolute_path': path.join(dirname, 'images', 'logo_institucion.png')
        },
        'entelai_img': {
            'type': 'image',
            'absolute_path': path.join(dirname, 'images', 'logo_entelai.png')
        },
        'title': 'Quality Report volumetria de cerebro',
        'table': {
            'rows': [
                ['Institución', 'Fecha del reporte'],
                [fake.name(), fake.date(pattern="%Y-%m-%d")]
            ]
        },
    }

    areas_2_table = {
        'type': 'table',
        'class': 'images-with-titles',
        'rows': [
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_0_1.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                 output_dir, 'corte_1_1.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_2_1.png')}],
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_3_1.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                 output_dir, 'corte_4_1.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_5_1.png')}],

        ]
    }

    areas_1_table = {
        'type': 'table',
        'class': 'images-with-titles',
        'rows': [
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_0_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                 output_dir, 'corte_1_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_2_0.png')}],
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_3_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                 output_dir, 'corte_4_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'corte_5_0.png')}],
        ]
    }

    lesiones_1_table = {
        'type': 'table',
        'class': 'images-with-titles',
        'rows': [
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_0_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                 output_dir, 'lesion_cut_peak_1_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_2_0.png')}],
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_3_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                 output_dir, 'lesion_cut_peak_4_0.png')},
             {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_5_0.png')}],
        ]
    }

    lesiones_2_table = {
        'type': 'table',
        'class': 'images-with-titles',
        'rows': [
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_0_1.png')},
                {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                    output_dir, 'lesion_cut_peak_1_1.png')},
                {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_2_1.png')}],
            [{'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_3_1.png')},
                {'type': 'image', 'width': '28%', 'absolute_path': path.join(
                    output_dir, 'lesion_cut_peak_4_1.png')},
                {'type': 'image', 'width': '28%', 'absolute_path': path.join(output_dir, 'lesion_cut_peak_5_1.png')}],
        ]
    }

    return {
        'components': [{
            'type': 'page',
            'components': [
                header,
                {
                    'type': 'main',
                    'components': [
                        {
                            'type': 'title',
                            'text': 'Métricas'
                        },
                        {
                            'type': 'table',
                            'class': 'data-table',
                            'header': ['Estructura', 'Dice'],
                            'rows': [
                                ['Segmentación de cerebro', '0.96'],
                                ['Segmentación de áreas', '0.82']
                            ]
                        },
                        {
                            'type': 'title',
                            'text': 'Segmentación de tejidos',
                        },
                        areas_1_table]
                },

                {
                    'type': 'footer',
                    'page_counter': '1',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }, {
            'type': 'page',
            'components': [
                header,
                {
                    'type': 'main',
                    'components': [
                        areas_2_table]
                },

                {
                    'type': 'footer',
                    'page_counter': '1',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }, {
            'type': 'page',
            'components': [
                header,
                {
                    'type': 'main',
                    'components': [
                        {
                            'type': 'title',
                            'text': 'Segmentación de lesiones',
                        },
                        lesiones_1_table]
                },

                {
                    'type': 'footer',
                    'page_counter': '1',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }, {
            'type': 'page',
            'components': [
                header,
                {
                    'type': 'main',
                    'components': [

                        lesiones_2_table]
                },

                {
                    'type': 'footer',
                    'page_counter': '1',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }
        ]
    }


def fake_study():
    return {'components': [{'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte'],
                                                    ['FLENI', '20-09-2019']]}},
                                {'type': 'main',
                                 'components': [{'type': 'title', 'text': 'Métricas'},
                                                {'type': 'table',
                                                 'class': 'data-table',
                                                 'header': ['Estructura', 'Dice'],
                                                 'rows': [['Segmentación de cerebro', 0.9822644628066077],
                                                          ['Segmentación de áreas', 0.8251768594571497]]},
                                                {'type': 'title', 'text': 'Segmentación de tejidos'}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '1']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_0_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_1_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_2_0.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_3_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_4_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_5_0.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '1']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_0_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_1_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_2_1.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_3_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_4_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/corte_5_1.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '1']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_0_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_1_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_2_0.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_3_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_4_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_5_0.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '1']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_0_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_1_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_2_1.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_3_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_4_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/1/lesion_cut_peak_5_1.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '2']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_0_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_1_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_2_0.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_3_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_4_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_5_0.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '2']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_0_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_1_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_2_1.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_3_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_4_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/corte_5_1.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '2']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_0_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_1_0.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_2_0.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_3_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_4_0.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_5_0.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]},
                {'type': 'page',
                 'components': [{'type': 'header',
                                 'main_img': {'type': 'image',
                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_institucion.png'},
                                 'entelai_img': {'type': 'image',
                                                 'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/logo_entelai.png'},
                                 'title': 'Quality Report volumetria de cerebro',
                                 'table': {'rows': [['Institución', 'Fecha del reporte', 'Id de estudio'],
                                                    ['FLENI', '20-09-2019', '2']]}},
                                {'type': 'main',
                                 'components': [{'type': 'table',
                                                 'class': 'images-with-titles',
                                                 'rows': [[{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_0_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_1_1.png'},
                                                           {'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_2_1.png'}],
                                                          [{'type': 'image',
                                                            'width': '28%',
                                                            'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_3_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_4_1.png'},
                                                           {'type': 'image',
                                                              'width': '28%',
                                                              'absolute_path': '/home/fran/repos/entelai-quality-report/reporter/images/2/lesion_cut_peak_5_1.png'}]]}]},
                                {'type': 'footer',
                                 'page_counter': '1',
                                 'disclaimer': 'Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.'}]}]}


def fake_volumetria():
    header = {
        'type': 'header',
        'main_img': {
            'type': 'image',
            'absolute_path': path.join(dirname, 'images', 'logo_institucion.png')
        },
        'entelai_img': {
            'type': 'image',
            'absolute_path': path.join(dirname, 'images', 'logo_entelai.png')
        },
        'title': 'Informe volumetria de cerebro',
        'table': {
            'rows': [
                ['Paciente', 'ID de Paciente',
                    'Nombre del estudio', 'Fecha del estudio'],
                [fake.name(), fake.phone_number(), fake.sentence(
                    nb_words=3), fake.date(pattern="%Y-%m-%d")],
                ['Edad', 'Género', 'Nombre estudio previo', 'Fecha estudio previo'],
                [random.randint(10, 80), random.choice(["Masculino", "Femenino"]), fake.sentence(nb_words=3),
                 fake.date(pattern="%Y-%m-%d")],
            ]
        },
    }
    sidebar = {
        'type': 'sidebar',
        'components': [{
            'type': 'title',
            'text': 'SEÑAL DEL PARENQUIMA'
        }, {
            'type': 'paragraph',
            'text': 'Múltiples imágenes focales y confluentes, de señal hiperintensa en FLAIR y T2 que comprometen la sustancia bihemisférica, a valorar según datos clínicos (Fazekas grado III).'
        }, {
            'type': 'title',
            'text': 'HIPOCAMPOS'
        }, {
            'type': 'paragraph',
            'text': 'Marcada reducción del volumen hipocampal bilateral. (MTA 4 bilateral)'
        }, {
            'type': 'title',
            'text': 'CISTERNAS Y SURCOS'
        }, {
            'type': 'paragraph',
            'text': 'Los valores de Fracción de parénquima cerebral (FPC) se encuentran por debajo del rango normal. Profundización de surcos y cisternas, a predominio parietal (GCA 3, Koedam grado 2)'
        }, {
            'type': 'title',
            'text': 'SISTEMA VENTRICULAR'
        }, {
            'type': 'paragraph',
            'text': 'Ampliación simétrica moderada del sistema ventricular supratentorial sin signos de evolutividad. Indice de Evans anormal.'
        }, {
            'type': 'title',
            'text': 'TRONCO ENCEFÁLICO'
        }, {
            'type': 'paragraph',
            'text': 'Disminución del volumen mesencefálico. Ratio área mesencefálisa / área protuberancial 0.1.'
        }, {
            'type': 'paragraph',
            'text': 'Atrofia cerebelosa asociado a atrofia protuberancial.'
        }]
    }
    main = {
        'type': 'main',
        'components': [
            {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    ['Volumen cerebro (FPC)',
                     'Volumen sustancia gris cortical'],
                    [{'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_fpc.png')},
                     {'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_sust_gris.png')}],
                    ['Volumen hipocampos', 'Indice de evans'],
                    [{'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_hipocampo.png')},
                     {'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_talamo.png')}],
                    ['Ratio mes/prot', 'Volumen cerebelo'],
                    [{'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_fpc.png')},
                     {'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_sust_gris.png')}],
                ]
            },
            {
                'type': 'title',
                'text': 'Segmentación de tejidos',
            },
            {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    [{'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'tejidos_y_estructuras_coronal.png')},
                     {'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'tejidos_y_estructuras_sagital.png')},
                     {'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'tejidos_y_estructuras_axial.png')}],
                ]
            }, {
                'type': 'title',
                'text': 'Mapa de calor de volumen según área'
            }, {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    [{'type': 'image', 'width': '28%',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_frontal.png')},
                     {'type': 'image', 'width': '28%',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_lateral.png')},
                     {'type': 'image', 'width': '28%',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_superior.png')},
                     {'type': 'vertical-gradient', 'width': '14%', 'stops': ['#5858d8', '#69eaea', '#45ab45'],
                      'values': ['1.0', '0.5', '0.0', '-0.5', '-1.0']}],
                ]
            }
        ]
    }
    return {
        'components': [{
            'type': 'page',
            'components': [
                header,
                sidebar,
                main,
                {
                    'type': 'footer',
                    'page_counter': '1',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }, {
            'type': 'page',
            'components': [
                header,
                {
                    'type': 'main',
                    'components': [
                        {
                            'type': 'title',
                            'text': 'Volumen segun estructuras'
                        },
                        {
                            'type': 'table',
                            'class': 'data-table',
                            'header': ['Estructura', 'Volumen', 'Rango normal ajustado por edad',
                                       'Percentilo normativo', 'Cambio volumen anualizado',
                                       'Cambio volumen anualizado normativo'],
                            'rows': [
                                ['Amigdala', '0.424', '0.845',
                                    '55.21', '342', '44'],
                                ['Caudado', '1e-23', '0.231',
                                    '0.4422', '1e-22', '0.12'],
                                ['Freesurfer', '55.21', '342',
                                    '0.424', '1e-23', '55.21'],
                                ['Glandula', '84.12', '2.34e2',
                                    '0.424', '0.845', '55.21'],
                                ['Canal #123', '1e-23', '0.231',
                                    '0.4422', '1e-22', '0.12'],
                                ['Barrilete cosmico', '2.334e2',
                                    '1e-23', '0.231', '0.424', '0.845'],
                                ['Tronco encefalico', '55.21', '342',
                                    '0.424', '1e-23', '55.21'],
                                ['Canal #234', '1e-23', '0.231',
                                    '0.4422', '1e-22', '0.12'],
                                ['Caudado', '1e-23', '0.231',
                                    '0.4422', '1e-22', '0.12'],
                                ['Glandula', '84.12', '2.34e2',
                                    '0.424', '0.845', '55.21'],

                            ]
                        }
                    ]
                }, {
                    'type': 'footer',
                    'page_counter': '2',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }]
    }


def fake_desmielinizantes():
    header = {
        'type': 'header',
        'main_img': {
            'type': 'image',
            'absolute_path': path.join(dirname, 'images', 'logo_institucion.png')
        },
        'entelai_img': {
            'type': 'image',
            'absolute_path': path.join(dirname, 'images', 'logo_entelai.png')
        },
        'title': 'Informe desmielinizantes',
        'table': {
            'rows': [
                ['Paciente', 'ID de Paciente',
                    'Nombre del estudio', 'Fecha del estudio'],
                [fake.name(), fake.phone_number(), fake.sentence(
                    nb_words=3), fake.date(pattern="%Y-%m-%d")],
                ['Edad', 'Género', 'Nombre estudio previo', 'Fecha estudio previo'],
                [random.randint(10, 80), random.choice(["Masculino", "Femenino"]), fake.sentence(nb_words=3),
                 fake.date(pattern="%Y-%m-%d")],
            ]
        },
    }
    sidebar = {
        'type': 'sidebar',
        'components': [{
            'type': 'title',
            'text': 'Detección de lesiones'
        }, {
            'type': 'paragraph',
            'text': 'Se detectan lesiones hiperintensas en la secuencia de FLAIR volumétrica a nivel periventricular, yuxtacortical, cortical, protuberancia, cerebelo.'
        }, {
            'type': 'paragraph',
            'text': 'Se cuantificó el volumen total de lesiones hiperintensas en FLAIR en XX cm3, en comparación con estudio previo fechado en XX/XX/XXXX, en donde había una carga lesional de XXcm3, notándose una diferencia de +0.5% (no significativa).'
        }, {
            'type': 'paragraph',
            'text': 'Se cuantificó el volumen total de lesiones hipointensas en T1 en XX cm3, en comparación con estudio previo fechado en XX/XX/XXXX, en donde había una carga lesional de XXcm3, notándose una diferencia de +0.01% (no significativa)'
        }, {
            'type': 'title',
            'text': 'Volumetria de cerebro'
        }, {
            'type': 'paragraph',
            'text': 'Los valores de Fracción de parénquima cerebral (FPC) se encuentra por debajo del rango normal.'
        }]
    }
    main = {
        'type': 'main',
        'components': [
            {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    ['Volumen cerebro (FPC)',
                     'Volumen sustancia gris cortical'],
                    [{'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_fpc.png')},
                     {'type': 'image', 'absolute_path': path.join(dirname, 'images', 'vol_sust_gris.png')}]
                ]
            }, {
                'type': 'br'
            }, {
                'type': 'title',
                'text': 'Segmentación de tejidos',
            },
            {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    [{'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'tejidos_y_estructuras_coronal.png')},
                     {'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'tejidos_y_estructuras_sagital.png')},
                     {'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'tejidos_y_estructuras_axial.png')}],
                ]
            }, {
                'type': 'br'
            }, {
                'type': 'title',
                'text': 'Cuantificación de lesiones'
            }, {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    [{'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_frontal.png')},
                     {'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_lateral.png')},
                     {'type': 'image',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_superior.png')}],
                ]
            }, {
                'type': 'br'
            }, {
                'type': 'table',
                'rows': [[{'type': 'reference', 'color': '#ea6aea', 'text': 'Lesiones hiperintensas FLAIR'},
                          {'type': 'reference', 'color': '#eeae6f', 'text': 'Lesiones Gadolinio positvas'}]]
            }, {
                'type': 'br'
            }, {
                'type': 'br'
            }, {
                'type': 'title',
                'text': 'Mapa de calor de volumen según área'
            }, {
                'type': 'table',
                'class': 'images-with-titles',
                'rows': [
                    [{'type': 'image', 'width': '28%',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_frontal.png')},
                     {'type': 'image', 'width': '28%',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_lateral.png')},
                     {'type': 'image', 'width': '28%',
                      'absolute_path': path.join(dirname, 'images', 'mapa_atrofia_superior.png')},
                     {'type': 'vertical-gradient', 'width': '14%', 'stops': ['#5858d8', '#69eaea', '#45ab45'],
                      'values': ['1.0', '0.5', '0.0', '-0.5', '-1.0']}],
                ]
            }
        ]
    }
    return {
        'components': [{
            'type': 'page',
            'components': [
                header,
                sidebar,
                main,
                {
                    'type': 'footer',
                    'page_counter': '1',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }, {
            'type': 'page',
            'components': [
                header,
                {
                    'type': 'main',
                    'components': [
                        {
                            'type': 'title',
                            'text': 'Analisis volumetrico de lesiones'
                        },
                        {
                            'type': 'table',
                            'class': 'data-table',
                            'header': ['Volumen de lesion', 'Estudio actual', 'Estudio anterior'],
                            'rows': [
                                ['Hiperintensas en flair (cm3)',
                                 '0.424', '0.845'],
                                ['Hiperintensas en flair (%VIC)',
                                 '1e-23', '0.231'],
                                ['Gadolinio positivas (cm3)', '55.21', '342'],
                                ['Gadolinio positivas (%VIC)',
                                 '84.12', '2.34e2']

                            ]
                        },
                        {
                            'type': 'title',
                            'text': 'Volumen segun estructuras'
                        },
                        {
                            'type': 'table',
                            'class': 'data-table',
                            'header': ['Estructura', 'Volumen', 'Rango normal ajustado por edad',
                                       'Percentilo normativo', 'Cambio volumen anualizado',
                                       'Cambio volumen anualizado normativo'],
                            'rows': [
                                ['Amigdala', '0.424', '0.845',
                                    '55.21', '342', '44'],
                                ['Caudado', '1e-23', '0.231',
                                    '0.4422', '1e-22', '0.12'],
                                ['Freesurfer', '55.21', '342',
                                    '0.424', '1e-23', '55.21'],
                                ['Glandula', '84.12', '2.34e2',
                                    '0.424', '0.845', '55.21'],
                                ['Canal #123', '1e-23', '0.231',
                                    '0.4422', '1e-22', '0.12'],
                                ['Barrilete cosmico', '2.334e2',
                                    '1e-23', '0.231', '0.424', '0.845']

                            ]
                        }
                    ]
                }, {
                    'type': 'footer',
                    'page_counter': '2',
                    'disclaimer': "Este reporte está aprobado para uso clínico en Argentina. Entelai Pic versión 2.0.0.",
                }
            ]
        }]
    }
