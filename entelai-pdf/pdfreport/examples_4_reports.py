import csv, os
import gettext
from os import path
from report_generator import ReportGenerator
import random
from os import path, makedirs
from pprint import pprint

# TODO: Esta linea futuramente tendra que ser borrada ya que _ va a venir definido
_ = gettext.gettext

class ReportData(object):

    TABLE_AREAS = ['TBD']

    def __init__(self):
        self.patient_name = 'Nombre de Prueba'
        self.patient_id = '12345678'
        if len(self.patient_name) > 30:
            self.patient_name = self.patient_name[:12] + ' ... ' + self.patient_name[-12:]
        if len(self.patient_id) > 30:
            self.patient_id = self.patient_id[:12] + ' ... ' + self.patient_id[-12:]
        self.gender = 'X'
        self.output_dir = './outputs'
        self.age = 55
        self.title = 'Titulo'
        self.study_name = 'Resonancia'
        date_string = '20010101'
        self.study_date = date_string[6:8] + '/' + date_string[4:6] + '/' + date_string[:4]
        self.prev_study_name = '-'
        self.prev_study_date = '-'
        self.main = None  # To be defined by subclass
        self.header = {
                'type': 'header',
                'main_img': {
                    'type': 'image',
                    'absolute_path': '../images/logo_institucion.png'
                },
                'entelai_img': {
                    'type': 'image',
                    'absolute_path': '../images/logo_entelai.png'
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


        self.sidebar = self.load_sidebar_text()

    def footer(self, pagenum):
        FOOTER = {
            'type': 'footer',
            'page_counter': '{}'.format(pagenum),
            'disclaimer': _("VIC: Volumen Intracraneal. Los rangos de valores normales están definidos al nivel del percentil 5%. Producto médico autorizado por ANMAT e inscripto en el Registro Nacional de Productores y Productos de Tecnología Médica bajo el número 2477-1. Entelai Pic versión 2.1.0."),
        }
        return FOOTER


    def generate_volume_table(self):
        rows = []
        for i in range(30):
            normative_percentile = 50
            volume = 15
            str_volume = '{:1.2f}%'.format(volume)
            range_low = 25
            range_high = 50
            str_range = '( {:1.2f} - {:1.2f} )'.format(range_low, range_high)
            print_name = 'Area {:0>2}'.format(i)
            values = [_(print_name), str_volume, str_range, normative_percentile] + ['-'] * 2
            if random.random() > 0.75:
                row = {'style': 'font-weight: bold', 'values': values}
            else:
                row = {'style': '', 'values': values}
            rows.append(row)
        return sorted(rows, key=lambda x: x['values'])

    def load_sidebar_text(self):
        """ To be defined by children"""
        return None

    def get_report_data(self):
        self.sidebar = self.load_sidebar_text()
        report_data = {
            'components': [{
                'type': 'page',
                'components': [
                    self.header,
                    self.sidebar,
                    self.main,
                    self.footer(1)
                ]
            }, {
                'type': 'page',
                'components': [
                    self.header,
                    self.main2,
                    self.footer(2)
                ]
            }, {
                'type': 'page',
                'components': [
                    self.header,
                    self.main3,
                    self.footer(3)
                ]
            }

            ]
                    }
        return report_data


class NeuroReportData(ReportData):
    TABLE_AREAS = ['TBD']
    #SIDEBAR_MAX_CHARACTERS = 1000

    def __init__(self):
        super().__init__()
        self.header = {}


    def create_reference_row(self, width, reference, label_class, reference_description):
        column = {
            'values': [
                {
                    'width': width.__str__()+'%',
                    'value': reference
                },
                {
                    'items': [
                        {
                            'type': 'span',
                            'class': label_class,
                            'text': reference_description
                        }
                    ]
                },
            ]
        }
        return column

    def create_volumetria_image_column(self, width, reference, image_abs_path, image_class ='image-center', style = None):
        column = {
            'width': width.__str__() + '%',
            'style': style if style is not None else '',
            'valign': 'top',
            'items': [
                {
                    'type': 'subtitle',
                    'text': reference
                },
                {
                    'type': 'image',
                    'absolute_path': image_abs_path,
                    'class': image_class
                }
            ],
        }
        return column


    @staticmethod
    def instructions():
        pass

    def generate_fake_table(self, quantity_rows):
        table_component = {
            'type': 'table',
            'class': 'striped-table data-table',
            'header': [
                {'value': _('Estructura'), 'style': 'width: 100px'},
                {'value': _('Vol. cm3'), 'style': 'width: 70px'},
                {'value': _('Vol. em %VIC'), 'style': 'width: 50px'},
                {'value': _('Faixa normal ajustada paraa idade de acordo com %VIC'), 'style': 'width: 95px'},
                {'value': _('Porcentil normativo'), 'style': 'width: 80px'},
                {'value': _('Variacao de percentil'), 'style': 'width: 80px'},
                {'value': _('Taxa de variacao anualizada'), 'style': 'width: 50px'},
            ],
            'rows': self.generate_fake_volume_table(quantity_rows)
        }

        return table_component

    def generate_fake_volume_table(self, quantity):
        rows = []
        for i in range(quantity):
            data = ['Nome do Item 1','1,185','77,61%',	'(68,72 - 90,96)','25,1','1,70 pp',	'0,36%']
            new_row = { 'values': data }
            rows.append(new_row)
        return rows

    def _set_sidebar_font(self):
        pass

    def footer(self, pagenum):
        FOOTER = {
            'type': 'footer',
            'detail': 'Pág {}'.format(pagenum),
        }
        return FOOTER

    def load_sidebar_text(self):
        """ Basic sidebar unless overridden by children"""
        sidebar = {
            'type': 'sidebar',
            'components': [
                {
                    'type': 'div',
                    'class': 'logo-container',
                    'items': [
                        {
                            'type': 'image',
                            'absolute_path': '../images/logo-cimacsj.png',
                        },
                    ]
                },
                {
                    'type': 'div',
                    'class': 'patient',
                    'items': [
                        {
                            'type': 'div',
                            'class': 'bloque-espaciado',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'text': _('Paciente')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': 'Quico',
                                },
                            ]
                        },
                        {
                            'type': 'div',
                            'class': 'bloque-espaciado',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'text': _('ID de Paciente')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': self.patient_id,
                                },
                            ]
                        },
                        {
                            'type': 'div',
                            'class': 'bloque-espaciado',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'text': _('Edad')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': self.age,
                                },
                            ]
                        },
                        {
                            'type': 'div',
                            'class': 'bloque-espaciado',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'text': _('Género')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': self.gender,
                                },
                            ]
                        },
                        {
                            'type': 'div',
                            'class': 'bloque-espaciado',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'text': _('Fecha del estudio')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': self.study_date,
                                },
                            ]
                        },
                    ],
                },
                {
                    'type': 'div',
                    'class': 'legal',
                    'items': [
                        {
                            'type': 'span',
                            'text': 'Powered by',
                        },
                        {
                            'type': 'image',
                            'absolute_path': '../images/entelai.png',
                            'class': 'logo-entelai',
                        },
                        {
                            'type': 'paragraph',
                            'class': 'con-mas-interlineado',
                            'text': _('Produto médico autorizado pela ANMAT e registrado no Registro Nacional de Produtores e Produtos de Tecnologia Médica (sob o número 2477-1) e ANVISA (sob o número 80102512470). Entelai Pic. versão v4.3.0')
                        },
                    ]
                },
            ],
        }
        return sidebar

    def get_report_data(self):
        self.sidebar = self.load_sidebar_text()
        self._set_sidebar_font()
        report_data = {
            'components': [{
                'type': 'page',
                'class': '',
                'components': [
                    #self.header,
                    self.sidebar,
                    self.main,
                ]
            }, {
                'type': 'page',
                'class': '',
                'components': [
                    #self.header,
                    self.sidebar,
                    self.main2,
                ]
            }, {
                'type': 'page',
                'class': '',
                'components': [
                    #self.header,
                    self.sidebar,
                    self.main3,
                ]
            }

            ]
        }
        return report_data


class VolumetriaReportData(NeuroReportData):

    def __init__(self):
        super().__init__()
        self.main = {
            'type': 'main',
            'components': [
                {
                    'type': 'div',
                    'class': 'content',
                    'items': [
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': _('Volumetría')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': _('Principais descobertas'),
                                    'class': 'subtitle'
                                },
                                {
                                    'type': 'table',
                                    'rows': [
                                        {'values': [
                                            {
                                                'width': '50%',
                                                'valign': 'top',
                                                'items': [
                                                    {
                                                        'type': 'table',
                                                        'class': 'featured-table striped-table',
                                                        'style': 'padding-right: 10px;',
                                                        'rows': [
                                                            self.create_reference_row(75, _('QC Index'),
                                                                                           'label label-yellow',
                                                                                      _('Moderada')),
                                                            self.create_reference_row(75, _('Brain Volumen'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Frontal'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Temporal'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Parietal'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Occipital'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Ventricles'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Brainstem 1'),
                                                                                        'label label-red',
                                                                                      _('Alta')),
                                                        ]
                                                    }
                                                ]
                                            },
                                            {
                                                'width': '50%',
                                                'valign': 'top',
                                                'items': [
                                                    {
                                                        'type': 'table',
                                                        'class': 'featured-table striped-table',
                                                        'style': 'padding-right: 10px;',
                                                        'rows': [
                                                            self.create_reference_row(75, _('Left Hippocampus'),
                                                                                        'label label-yellow',
                                                                                      _('Moderada')),
                                                            self.create_reference_row(75, _('Right Hippocampus'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('HAI'),
                                                                                            'label label-green',
                                                                                          _('Baja')),
                                                            self.create_reference_row(75, _('Parahippocampal cortex'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Entorhinal cortex'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Inferior parietal lobule'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Precuneus'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Cuneus'),
                                                                                        'label label-red',
                                                                                      _('Alta')),
                                                        ]
                                                    }
                                                ]
                                            },
                                        ]},
                                    ],
                                },
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('Brain Volume'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('SB. Volume'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('L. vol sg. total'),
                                                                                      '../images/img1.jpg'),
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('SG. Costial'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Hippoc. Der'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Hipocampo izquierdo'),
                                                                                      '../images/img1.jpg'),
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('Ventrículos'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Asimetría'),
                                                                                      '../images/img2.jpg'),
                                                self.create_volumetria_image_column(33, _('Radar'),
                                                                                      '../images/img3.jpg'),
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': 'Mapa de Calor',
                                },
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('Carga lesional'),
                                                                                      '../images/img4.jpg',
                                                                                      'image-center',
                                                                                      ';padding-right: 10px'),
                                                self.create_volumetria_image_column(33, _('Subcortical'),
                                                                                      '../images/img5.jpg',
                                                                                      'image-center',
                                                                                      ';padding-right: 10px'),
                                                self.create_volumetria_image_column(33, _('Cortical'),
                                                                                    '../images/img5.jpg',
                                                                                    'image-center',
                                                                                    ';padding-right: 10px'),
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'type': 'div',
                                    'class': 'description',
                                    'items': [
                                        {
                                            'type': 'span',
                                            'class': 'swatch teal-bg'
                                        },
                                        {
                                            'type': 'h3',
                                            'text': 'Área a analisar',
                                        },
                                        {
                                            'type': 'span',
                                            'class': 'swatch red-bg'
                                        },
                                        {
                                            'type': 'h3',
                                            'text': 'Área possivelmente atrófica',
                                        },
                                    ],
                                }
                            ],
                        },
                    ],
                },
                self.footer(1),
            ]
        }

        self.main2 = {
                    'type': 'main',
                    'components': [
                        {
                            'type': 'div',
                            'class': 'content',
                            'items': [
                                {
                                    'type': 'div',
                                    'items': [
                                        {
                                            'type': 'title',
                                            'text': _('Volumetria'),
                                        },
                                        {
                                            'type': 'subtitle',
                                            'class': 'izquierda',
                                            'text': _('Título 1'),
                                        },
                                        self.generate_fake_table(6),
                                    ],
                                },
                                {
                                    'type': 'div',
                                    'class': 'tabla-aireada',
                                    'items': [
                                        {
                                            'type': 'subtitle',
                                            'class': 'izquierda',
                                            'text': _('Título 2'),
                                        },
                                        self.generate_fake_table(10),
                                    ],
                                },
                                {
                                    'type': 'div',
                                    'class': 'tabla-aireada',
                                    'items': [
                                        {
                                            'type': 'subtitle',
                                            'class': 'izquierda',
                                            'text': _('Título 3'),
                                        },
                                        self.generate_fake_table(2),
                                    ],
                                },
                                {
                                    'type': 'div',
                                    'class': 'tabla-aireada',
                                    'items': [
                                        {
                                            'type': 'subtitle',
                                            'class': 'izquierda',
                                            'text': _('Título 4'),
                                        },
                                        self.generate_fake_table(5),
                                    ],
                                },
                            ],
                        },
                        self.footer(2),
                    ]
        }

        self.main3 = {
            'type': 'main',
            'components': [
                {
                    'type': 'div',
                    'class': 'content',
                    'items': [
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': _('Volumetria'),
                                },
                                {
                                    'type': 'subtitle',
                                    'text': _('Título 1'),
                                    'class': 'izquierda',
                                },
                                self.generate_fake_table(28),
                            ],
                        },
                        {
                            'type': 'div',
                            'class': 'annotations border-box',
                            'items': [
                                {
                                    'type': 'h3',
                                    'text': _('Aclaraciones para el médico')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': _('Abreviaturas: VIC (Volume Intracraniano).')
                                },
                                {
                                    'type': 'paragraph',
                                    'class': 'indicaciones-max',
                                    'text': _('As faixas normais correspondem a valores contidos entre o percentil 1% e 99%. As áreas abaixo do limite inferior (superior no caso do sistema ventricular) são destacadas em negrito.')
                                },
                                {
                                    'type': 'paragraph',
                                    'items': [
                                        {
                                            'type': 'span',
                                            'class': 'label-icon label-green',
                                            'items': [
                                                {
                                                    'type': 'image',
                                                    'absolute_path': '../images/chevron-down-solid.png',
                                                    'class': 'img-icono svg-green'
                                                },
                                            ],
                                        },
                                        _('A diminuição anual do volume desta área é maior do que o esperado para a faixa etária (exceto estruturas subcorticais).'),
                                    ],
                                },
                                {
                                    'type': 'paragraph',
                                    'items': [
                                        {
                                            'type': 'span',
                                            'class': 'label-icon label-red',
                                            'items': [
                                                {
                                                    'type': 'image',
                                                    'absolute_path': '../images/chevron-up-solid.png',
                                                    'class': 'img-icono svg-red'
                                                },
                                            ],
                                        },
                                        _('O aumento anual do volume desta área é maior do que o esperado para a faixa etária (exceto estruturas subcorticais).'),
                                    ],
                                },
                            ]
                        }
                    ],
                },
                self.footer(3),
            ]
        }

class ReportDataTorax(object):
    FOOTER = {
                'type': 'footer',
                'page_counter': '1',
                'disclaimer': _("Entelai Pic Radiografía de Torax Versión 1.0.0. Producto médico en proceso de autorización por la ANMAT."),
             }

    def __init__(self):
        #self.patient_name = study['PatientMainDicomTags']['PatientName'].replace('^', ', ').title()
        self.patient_name = 'patient name'
        self.patient_id = '12312312'
        #self.patient_id = 'patient id'
        #self.gender = study['PatientMainDicomTags']['PatientSex']
        self.gender = 'gender'
        self.output_dir = output_dir

        self.dict_proj = {'AP': 'frente', 'PA': 'frente', 'LAT': 'perfil'}
        # Diccionario de proyecciones

        #self.table = pd.read_csv(path.join(self.output_dir, FNAME_RESULTS_TABLE_TORAX))
        #self.table2 = self.table.reset_index()
        #self.table = self.table.set_index(['Exam'])
        #print(self.table)
        #self.table.to_csv(path.join(output_dir, 'FNAME_RESULTS_TABLE_TORAX.csv'))
        # Remove Dispositivos externos/material quirúrgico row FIXME
        #self.table = self.table[self.table['Exam'] != 'Dispositivos externos/material quirúrgico']
        #print(self.table)
        self.age = 50

        self.output_dir = output_dir
        self.title = _('Reporte Torax')
        self.study_name = '-'
        #self.study_name = study['MainDicomTags']['StudyDescription'].title()
        #date_string = study['MainDicomTags']['StudyDate']
        #self.study_date = date_string[6:8] + '/' + date_string[4:6] + '/' + date_string[:4]
        self.study_date = "date"
        self.prev_study_name = '-'
        self.prev_study_date = '-'
        self.main = None  # To be defined by subclass
        self.header = {
                'type': 'header',
                'main_img': {
                    'type': 'image',
                    'absolute_path': '../images/logo_entelai.png'
                },
                #'entelai_img': {
                #    'type': 'image',
                #    'absolute_path': path.join('.', 'images', 'LOGO_ENTELAI.png')
                #},
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

        self.main = {
            'type': 'main',
            'components': [
                           {
                'type': 'table',
                'class': 'images-with-titles',
                'header': ['Áreas de interés'],
                'rows': [
                    [_('Proyección  LAT')],
                    [{'type': 'image','absolute_path': '../images/pred_img_report_1.png'}],
                    [_('Proyección ') + _('AP')],
                    [{'type': 'image','absolute_path': '../images/pred_img_report_2.png'}]
                    #[{'type': 'image','absolute_path': path.join(output_dir, 'pred_img' + str(2) + '_report.png')}]
                    ]
            },
            {
                'type': 'br'
            }
            ]
                }


        #self.sidebar = self.load_sidebar_text()



    def load_abnormal_sidebar_text(self):
        text = _(
            'La siguiente radiografía de tórax se analizó utilizando un sistema de inteligencia artificial.'
            ' Se utilizó la imagen de XXX. Se observaron al menos una anormalidad en el estudio para revisión '
            'por el especialista.'
        )

        sidebar = {
            'type': 'sidebar',
            'components': [
               {
                'type': 'title',
                'text': _('Reporte de análisis automatizado por inteligencia artificial ')
            }, {'type': 'paragraph',
                    'text': text
                    },
           {
                'type': 'title',
                'text': _('Sospecha diagnóstica')
            }, {
                'type': 'paragraph',
                'text': _('El estudio presenta los siguientes hallazgos para evaluación:')
            },
            {'type': 'image',
            'absolute_path': path.join(self.output_dir, 'pred_img' + str(3) + '_report.png')
            }
]
        }
        return sidebar

    def load_normal_sidebar_text(self):

        text = _(
            'La siguiente radiografía de tórax se analizó utilizando un sistema de inteligencia artificial.'
            ' Se utilizaron las imágenes de frente y perfil.'
        )

        sidebar = {
            'type': 'sidebar',
            'components': [
               {
                'type': 'title',
                'text': _('Reporte de análisis automatizado por inteligencia artificial ')
            }, {'type': 'paragraph',
                    'text': text
                    },
           {
                'type': 'title',
                'text': _('Sospecha diagnóstica')
            }, {
                'type': 'paragraph',
                'text': _('No se detectaron hallazgos anormales.')
            }
]
        }
        return sidebar

    def load_pseudo_abnormal_sidebar_text(self):
        text = (
            'La siguiente radiografía de tórax se analizó utilizando un sistema de inteligencia artificial.'
            ' Se utilizaron las imágenes de frente y perfil.'
        )

        sidebar = {
            'type': 'sidebar',
            'components': [
               {
                'type': 'title',
                'text': _('Reporte de análisis automatizado por inteligencia artificial ')
            }, {'type': 'paragraph',
                    'text': text
                    },
           {
                'type': 'title',
                'text': _('Sospecha diagnóstica')
            }, {
                'type': 'paragraph',
                'text': _('Se observa un área anormal para revisión por el especialista.')
            }
]
        }
        return sidebar



    def get_report_data(self):

        self.sidebar = self.load_normal_sidebar_text()

        report_data = {
            'components': [{
                'type': 'page',
                'components': [
                    self.header,
                    self.sidebar,
                    self.main,
                    self.FOOTER
                ]
            }
            ]
                    }
        return report_data


class ThoraxV4ReportData(ReportData):
    def __init__(self):
        super().__init__()
        self.header["entelai_img"]["absolute_path"] = path.join(
            "..", "images", "logo_entelai-thorax.png"
        )

        self.main = self.load_main_section()
        self.sidebar = self.load_sidebar()
        self.header["table"] = {
            "rows": [
                [
                    _("Paciente"),
                    _("ID de Paciente"),
                    _("Nombre del estudio"),
                    _("Fecha del estudio"),
                ],
                [self.patient_name, self.patient_id, self.study_name, self.study_date],
                [_("Edad"), _("Género")],
                [self.age, self.gender],
            ]
        }

    def load_main_section(self):
        first_image_path = '../images/pred_img0_report.png'
        first_view = [
            [_("Proyección AP")],
            [
                {
                    "type": "image",
                    "absolute_path": first_image_path,
                    "style": "width:100%;",
                }
            ],
        ]


        desc_1 = "AP"
        second_image_path = "../images/no_bg_ori_img.png"
        desc_1 = "AP Original"

        second_view = [
            [_("Proyección ") + desc_1.upper()],
            [
                {
                    "type": "image",
                    "absolute_path": second_image_path,
                    "style": "width:100%;",
                }
            ],
        ]

        main = {
            "type": "main",
            "components": [
                {
                    "type": "table",
                    "class": "images-with-titles",
                    "header": [_("Áreas de interés")],
                    "rows": first_view + second_view,
                },
                {"type": "br"},
            ],
        }
        return main

    def load_sidebar(self):
        text = """La siguiente radiografía de tórax se analizó
utilizando un sistema de inteligencia
artificial. Se utilizó la imagen de frente. Se
observó al menos una anormalidad en el
estudio para revisión por el especialista.""" #self.findings["text"]
        diagnosis = """El estudio presenta los siguientes hallazgos
para evaluación:""" #self.findings["diagnosis"]
        findings = ['<span style="line-height:16px">&#8226</span> Revisar item (85%)']*5
       #self.findings["findings"]

        sidebar = {
            "type": "sidebar",
            "components": [
                {
                    "type": "div",
                    'class': 'relativo',
                    'items': [
                        {
                            "type": "title",
                            "text": _(
                                "Reporte de análisis automatizado por inteligencia artificial"
                            ),
                        },
                        {"type": "paragraph", "text": text},
                        {"type": "title", "text": _("Hallazgos radiológicos")},
                        {"type": "paragraph", "text": diagnosis},
                        {"type": "list", "class": 'item_hallazgo', "items": findings},
                        {
                            "type": "div",
                            "class": "fijo",
                            "items": [
                                {
                                    "type": "title",
                                    'class': 'titulo_reducido',
                                    "text": _("Aclaración para el médico"),
                                },
                                {
                                    "type": "paragraph",
                                    "text": _(
                                        "El porcentaje presente en cada hallazgo refleja el grado de certeza que posee "
                                        "el algoritmo para su predicción. Cuanto más alto el porcentaje,"
                                        "mayor es el grado de certeza ante un determinado hallazgo. "
                                        "Por el contrario, porcentajes más bajos, reflejan un menor grado de certeza."
                                        "Esto puede deberse a factores del entrenamiento del algoritmo o "
                                        "propios de la imagen (hallazgo pequeño, atípico o imagen de baja calidad)."
                                        "Los mapas de calor son una representación visual de los sectores de la radiografía"
                                        "que fueron más relevantes para el algoritmo de inteligencia artificial en su predicción."
                                        "Sin embargo, estas áreas pueden no necesariamente coincidir con"
                                        "los sectores radiológicamente relevantes para el diagnóstico del hallazgo."
                                    ),
                                    "class": "texto_reducido",
                                },
                                {
                                    "type": "title",
                                    'class': 'titulo_reducido',
                                    "text": _("Aclaración para el paciente"),
                                },
                                {
                                    "type": "paragraph",
                                    "text": _(
                                        "Este reporte es generado por un sistema de inteligencia artificial de soporte para"
                                        " uso exclusivo de los profesionales médicos. En consecuencia, este reporte no podrá"
                                        " considerarse como un diagnóstico médico ni como una opinión médica y, por tanto,"
                                        " no reemplaza el diagnóstico o la opinión médica del profesional responsable a cargo."
                                        " La información contenida en este informe no es exhaustiva ni podrá considerarse como"
                                        " tal y no queda exenta de cualquier limitación o error pudiendo incluso ser distinta"
                                        " a la opinión del médico tratante quien será el único profesional responsable"
                                        " capacitado para elaborar un diagnóstico. Siga siempre todas las recomendaciones del"
                                        " profesional médico tratante."
                                    ),
                                    "class": "texto_reducido",
                                },
                            ],
                        },
                    ]
                },

            ],
        }
        return sidebar

    def get_report_data(self):
        report_data = {
            "components": [
                {
                    "type": "page",
                    "class": "torax", #+ self.institution_logo_class,
                    "components": [
                        self.header,
                        self.sidebar,
                        self.main,
                        self.footer(1),
                    ],
                }
            ]
        }
        return report_data

class ReportDataMammo(object):
    FOOTER = {
                'type': 'footer',
                'page_counter': '1',
                'disclaimer': _(
                    "Entelai Pic Mamografía Versión 1.0.0. Producto médico autorizado por ANMAT e inscripto en el Registro Nacional de "
                    "Productores y Productos de Tecnología Médica bajo el número 2477-1."
                ),
             }

    def __init__(self):
        #self.patient_name = study['PatientMainDicomTags']['PatientName'].replace('^', ', ').title()
        self.patient_name = 'patient name'
        #self.patient_id = study['PatientMainDicomTags']['PatientID']
        self.patient_id = 'patient id'
        #self.gender = study['PatientMainDicomTags']['PatientSex']
        self.gender = 'gender'
        self.output_dir = output_dir
        self.dic_translate = {'LEFT-CC':'Izquierda-CC', 'LEFT-MLO':'Izquierda-MLO', 'RIGHT-CC':'Derecha-CC', 'RIGHT-MLO':'Derecha-MLO'} #TODO
        #self.dic_birads = {-1:'0', 0:'2', 1:'3', 2:'4', 3:'5'} #TODO
        self.age = 50
        #self.output_dir = output_dir
        self.title = 'Reporte Mamografía'
        self.study_name = 'Estudio'
        #self.study_name = study
        #self.pred_birads = self.table.loc['bi-rads'].values[:,1]
        # replace nan values by -1
        #self.pred_birads = np.where(np.isnan(self.pred_birads), -1, self.pred_birads)
        #self.worst_cases_id = list(np.where(self.pred_birads == np.amax(self.pred_birads))[0]*4)
        #self.worst_cases = []
        #for i in range(len(self.worst_cases_id)):
        #    self.worst_cases.append(self.dic_translate[str(self.table.iloc[self.worst_cases_id[i]].name[1])])
        #self.study_name = study['MainDicomTags']['StudyDescription'].title()
        #date_string = study['MainDicomTags']['StudyDate']
        #self.study_date = date_string[6:8] + '/' + date_string[4:6] + '/' + date_string[:4]

        # save birads predictions for Quality Report
        #self.birads_patient = self.dic_birads[np.nanmax(self.pred_birads)]
        #f= open("/tmp/birads_predictions.txt","a+")
        #f.write(self.birads_patient)
        #f.write("\n")
        #f.close()

        self.study_date = "date"
        self.prev_study_name = '-'
        self.prev_study_date = '-'
        self.main = None  # To be defined by subclass
        self.header = {
                'type': 'header',
                'main_img': {
                    'type': 'image',
                    'absolute_path': '../images/logo_entelai.png'
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

        self.main = {
            'type': 'main',
            'components': [
                           {
                'type': 'table',
                'class': 'images-with-titles',
                'header': [_('Mamografía'), _('Áreas de interés')],
                'rows': [
                    [_('Derecha-MLO'), _('Derecha-MLO')],
                    [{'type': 'image', 'absolute_path': '../images/mammo_test1.png'}, {'type': 'image','absolute_path': '../images/mammo_test2.png'}],
                    [_('Derecha-CC'), _('Derecha-CC')],
                    [{'type': 'image', 'absolute_path': '../images/mammo_test3.png'}, {'type': 'image','absolute_path': '../images/mammo_test4.png'}],
                    [_('Izquierda-MLO'), _('Izquierda-MLO')],
                    [{'type': 'image', 'absolute_path': '../images/mammo_test5.png'}, {'type': 'image', 'absolute_path': '../images/mammo_test6.png'}],
                    [_('Izquierda-CC'), _('Izquierda-CC')],
                    [{'type': 'image', 'absolute_path': '../images/mammo_test7.png'}, {'type': 'image', 'absolute_path': '../images/mammo_test8.png'}],
                ]
            },
            {
                'type': 'br'
            }
            ]
                }


        #self.sidebar = self.load_sidebar_text()

    def calc_vs_mass_text(self, side):
        return _(' Se observó una anomalía correspondiente a una calcificación y una masa con una certeza mayor a 85%.')

    def ben_vs_mal_text(self, mama):
        return _(' Se estima con un 90%  de probabilidad la existencia de al menos una anomalía maligna.')


    def load_calc_mass_sidebar_text(self):
        text =  _(' (hallazgo en mama derecha)')
        # TODO: ver de usar ngettext('{0} Human', '{0} Humans', num)

        sidebar = {
            'type': 'sidebar',
            'components': [
                          {
                'type': 'title',
                'text': _('Reporte de inteligencia artificial')
            },
                {'type': 'paragraph',
                    #'text': 'Se analizaron las mamografías en las proyecciones craneocaudal y mediolateral oblicua de las mamas izquierda y derecha utilizando un algoritmo de inteligencia artificial. Se encontró al menos alguna anomalía con una certeza mayor a ' + str(int(np.nanmax(self.table.loc['norm vs abnorm'].values[:,1])*100)) + '%.'
                    'text': _(
                        'Se analizaron las mamografías en las proyecciones craneocaudal y mediolateral oblicua de las mamas izquierda y'
                        ' derecha utilizando un algoritmo de inteligencia artificial. Se observaron al menos una anormalidad en el estudio'
                        ' para revisión por el especialista.'
                    )
                    },
            {
                'type': 'title',
                'text': _('Hallazgos encontrados')
            }, {
                'type': 'title',
                'text': _('Mama Derecha')
            },
              {
                'type': 'paragraph',
                'text': self.calc_vs_mass_text('RIGHT')
            },{
                'type': 'title',
                'text': _('Mama Izquierda')
            },
            {
                'type': 'paragraph',
                'text': self.calc_vs_mass_text('LEFT')
            },
              {
                'type': 'title',
                'text': _('Clasificación segun BIRADS')
            }, {
                'type': 'paragraph',
                'text': _('Los hallazgos en la mamografía corresponden a un BIRADS de 3') + text
            }
]
        }
        return sidebar

    def load_abnormal_sidebar_text(self):
        sidebar = {
            'type': 'sidebar',
            'components': [
                          {
                'type': 'title',
                'text': _('Reporte de inteligencia artificial')
            },
                {'type': 'paragraph',
                    #'text': 'Se analizaron las mamografías en las proyecciones craneocaudal y mediolateral oblicua de las mamas izquierda y derecha utilizando un algoritmo de inteligencia artificial. Se encontró al menos alguna anomalía con una certeza mayor a ' + str(int(np.nanmax(self.table.loc['norm vs abnorm'].values[:,1])*100)) + '%.'
                    'text': _(
                        'Se analizaron las mamografías en las proyecciones craneocaudal y mediolateral oblicua de las mamas izquierda y '
                        'derecha utilizando un algoritmo de inteligencia artificial. Se observaron al menos una anormalidad en el estudio para '
                        'revisión por el especialista.'
                    )
                    },
              {
                'type': 'title',
                'text': _('Clasificación de estudio')
            }, {
                'type': 'paragraph',
                'text': _('Anormal')
            }
]
        }
        return sidebar

    def load_normal_sidebar_text(self):
        sidebar = {
            'type': 'sidebar',
            'components': [
               {
                'type': 'title',
                'text': _('Reporte de inteligencia artificial')
            }, {'type': 'paragraph',
                    #'text': 'Se analizaron las mamografías en las proyecciones craneocaudal y mediolateral oblicua de las mamas izquierda y derecha utilizando un algoritmo de inteligencia artificial. No se encontraron anomalías en ninguna de las mamas analizadas con una certeza mayor a ' + str(int(np.nanmax(self.table.loc['norm vs abnorm'].values[:,0])*100)) + '%.'
                    'text': _(
                        'Se analizaron las mamografías en las proyecciones craneocaudal y mediolateral oblicua de las mamas izquierda y '
                        'derecha utilizando un algoritmo de inteligencia artificial. No se encontraron anomalías en ninguna de las mamas analizadas.'
                    )
                    },
           {
                'type': 'title',
                'text': _('Clasificación de estudio')
            }, {
                'type': 'paragraph',
                'text': _('Normal')
            }
]
        }
        return sidebar



    def get_report_data(self):
        # if the algorithm predicts any abnormal image call abnormal report
        self.sidebar = self.load_normal_sidebar_text()
        report_data = {
            'components': [{
                'type': 'page',
                'components': [
                    self.header,
                    self.sidebar,
                    self.main,
                    self.FOOTER
                ]
            }
            ]
                    }
        return report_data

class DesmielinizantesReportData(NeuroReportData):

    def __init__(self):
        super().__init__()
        self.main = {
            'type': 'main',
            'components': [
                {
                    'type': 'div',
                    'class': 'content',
                    'items': [
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': _('Desmielinizantes')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': _('Principais descobertas'),
                                    'class': 'subtitle'
                                },
                                {
                                    'type': 'table',
                                    'rows': [
                                        {'values': [
                                            {
                                                'width': '50%',
                                                'valign': 'top',
                                                'items': [
                                                    {
                                                        'type': 'table',
                                                        'class': 'featured-table striped-table',
                                                        'style': 'padding-right: 10px;',
                                                        'rows': [
                                                            self.create_reference_row(75, _('QC Index'),
                                                                                        'label label-yellow',
                                                                                      _('Moderada')),
                                                            self.create_reference_row(75, _('Brain Volumen'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('White matter'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Gray matter'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Cerebelo'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Brainsterm 1'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('Left Thalamus'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Right Thalamus 1'),
                                                                                        'label label-red',
                                                                                      _('Alta')),
                                                        ]
                                                    }
                                                ]
                                            },
                                            {
                                                'width': '50%',
                                                'valign': 'top',
                                                'items': [
                                                    {
                                                        'type': 'table',
                                                        'class': 'featured-table striped-table',
                                                        'style': 'padding-right: 10px;',
                                                        'rows': [
                                                            self.create_reference_row(75, _('Graph lesion load tertiles'),
                                                                                        'label label-yellow',
                                                                                      _('Moderada')),
                                                            {
                                                                'values': [
                                                                    {
                                                                        'colspan': '2',
                                                                        'type': 'image',
                                                                        'absolute_path': '../images/img6.jpg',
                                                                        'style': 'height: 70px',
                                                                        'class': 'w-100'
                                                                    }
                                                                ]
                                                            },
                                                            self.create_reference_row(75, _('Stable lesions'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Enlarging lesions'),
                                                                                        'label label-green',
                                                                                      _('Baja')),
                                                            self.create_reference_row(75, _('New lesion'),
                                                                                        'label label-teal',
                                                                                      _('Minima')),
                                                            self.create_reference_row(75, _('Total lesion load'),
                                                                                        'label label-red',
                                                                                      _('Alta')),
                                                        ]
                                                    }
                                                ]
                                            },
                                        ]},
                                    ],
                                },
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('Brain Volume'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('SB. Volume'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('L. vol sg. total'),
                                                                                      '../images/img1.jpg'),
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('SG. Costial'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Hippoc. Der'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Hipocampo izquierdo'),
                                                                                      '../images/img1.jpg'),
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('Ventrículos'),
                                                                                      '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Asimetría'),
                                                                                      '../images/img2.jpg'),
                                                self.create_volumetria_image_column(33, _('Radar'),
                                                                                      '../images/img3.jpg'),
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': 'Mapa de Calor',
                                },
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(50, _('Deep'),
                                                                                      '../images/img4.jpg',
                                                                                      'w-100',
                                                                                      ';padding-right: 10px'),
                                                self.create_volumetria_image_column(50, _('Central'),
                                                                                      '../images/img5.jpg',
                                                                                      'w-100',
                                                                                      ';padding-left: 10px'),
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'type': 'div',
                                    'class': 'description',
                                    'items': [
                                        {
                                            'type': 'span',
                                            'class': 'swatch teal-bg'
                                        },
                                        {
                                            'type': 'h3',
                                            'text': 'Área a analisar',
                                        },
                                        {
                                            'type': 'span',
                                            'class': 'swatch red-bg'
                                        },
                                        {
                                            'type': 'h3',
                                            'text': 'Área possivelmente atrófica',
                                        },
                                    ],
                                }
                            ],
                        },
                    ],
                },
                self.footer(1),
            ]
        }

        self.main2 = {
            'type': 'main',
            'components': [
                {
                    'type': 'div',
                    'class': 'content',
                    'items': [
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': _('Volumetria'),
                                },
                                {
                                    'type': 'subtitle',
                                    'class': 'izquierda',
                                    'text': _('Título 1'),
                                },
                                self.generate_fake_table(6),
                            ],
                        },
                        {
                            'type': 'div',
                            'class': 'tabla-aireada',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'class': 'izquierda',
                                    'text': _('Título 2'),
                                },
                                self.generate_fake_table(10),
                            ],
                        },
                        {
                            'type': 'div',
                            'class': 'tabla-aireada',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'class': 'izquierda',
                                    'text': _('Título 3'),
                                },
                                self.generate_fake_table(2),
                            ],
                        },
                        {
                            'type': 'div',
                            'class': 'tabla-aireada',
                            'items': [
                                {
                                    'type': 'subtitle',
                                    'class': 'izquierda',
                                    'text': _('Título 4'),
                                },
                                self.generate_fake_table(5),
                            ],
                        },
                    ],
                },
                self.footer(2),
            ]
        }

        self.main3 = {
            'type': 'main',
            'components': [
                {
                    'type': 'div',
                    'class': 'content',
                    'items': [
                        {
                            'type': 'div',
                            'items': [
                                {
                                    'type': 'title',
                                    'text': _('Volumetria'),
                                },
                                {
                                    'type': 'subtitle',
                                    'text': _('Título 1'),
                                },
                                self.generate_fake_table(21),
                            ],
                        },
                        {
                            'type': 'div',
                            'class': 'annotations border-box',
                            'items': [
                                {
                                    'type': 'h3',
                                    'text': _('Aclaraciones para el médico')
                                },
                                {
                                    'type': 'paragraph',
                                    'text': _('Abreviaturas: VIC (Volume Intracraniano).')
                                },
                                {
                                    'type': 'paragraph',
                                    'class': 'indicaciones-max',
                                    'text': _(
                                        'As faixas normais correspondem a valores contidos entre o percentil 1% e 99%. As áreas abaixo do limite inferior (superior no caso do sistema ventricular) são destacadas em negrito.')
                                },
                                {
                                    'type': 'paragraph',
                                    'items': [
                                        {
                                            'type': 'span',
                                            'class': 'label-icon label-green',
                                            'items': [
                                                {
                                                    'type': 'image',
                                                    'absolute_path': '../images/chevron-down-solid.png',
                                                    'class': 'img-icono svg-green'
                                                },
                                            ],
                                        },
                                        _('A diminuição anual do volume desta área é maior do que o esperado para a faixa etária (exceto estruturas subcorticais).'),
                                    ],
                                },
                                {
                                    'type': 'paragraph',
                                    'items': [
                                        {
                                            'type': 'span',
                                            'class': 'label-icon label-red',
                                            'items': [
                                                {
                                                    'type': 'image',
                                                    'absolute_path': '../images/chevron-up-solid.png',
                                                    'class': 'img-icono svg-red'
                                                },
                                            ],
                                        },
                                        _('O aumento anual do volume desta área é maior do que o esperado para a faixa etária (exceto estruturas subcorticais).'),
                                    ],
                                },
                            ]
                        }
                    ],
                },
                self.footer(3),
            ]
        }

    def get_lesion_rows(self):

        rows = [
                [_('Hiperintensas en flair (cm3)'), 50, '-'],
                [_('Hiperintensas en flair (%VIC)'), 0.5, '-'],
                #['Gadolinio positivas (cm3)', active_volume, '-'], #  Not showing for now.
                #['Gadolinio positivas (%VIC)', active_volume_vic, '-']

                ]
        return rows


if __name__ == '__main__':
    output_dir = path.join(path.dirname(__file__), ".")
    if not path.exists(output_dir):
        makedirs(output_dir)

    # TODO: resolve how to define the language. At moment is fixed here
    try:
        locale_path = path.join(path.dirname(__file__),"../locale")
        language = 'en'
        os.environ['LANGUAGE'] = language

        lang = gettext.translation('messages', localedir=locale_path, languages=[language])
        lang.install()
        _ = lang.gettext

    except OSError as err:
        pprint(f'Traduccion no disponible - OS error: {err}')
        _ = gettext.gettext

    volumetria_report_file_path = path.join(output_dir, "reporte_volumetria.pdf")
    volumetria_report_data = VolumetriaReportData().get_report_data()
    pprint("Saving report to %s with data:" % volumetria_report_file_path)
    #pprint(volumetria_report_data)
    ReportGenerator.generate_report(out_path=volumetria_report_file_path, report=volumetria_report_data, required_new_templates=True)

    desmielinizantes_report_file_path = path.join(output_dir, "reporte_desmielinizantes.pdf")
    desmielinizantes_report_data = DesmielinizantesReportData().get_report_data()
    pprint("Saving report to %s with data:" % desmielinizantes_report_file_path)
    #pprint(desmielinizantes_report_data)
    ReportGenerator.generate_report(out_path=desmielinizantes_report_file_path, report=desmielinizantes_report_data, required_new_templates=True)

    thorax_report_file_path = path.join(output_dir, "reporte_torax.pdf")
    torax_report_data = ReportDataTorax().get_report_data()
    pprint("Saving report to %s with data:" % thorax_report_file_path)
    #pprint(desmielinizantes_report_data)
    ReportGenerator.generate_report(out_path=thorax_report_file_path, report=torax_report_data)

    mammo_report_file_path = path.join(output_dir, "reporte_mammo.pdf")
    mammo_report_data = ReportDataMammo().get_report_data()
    pprint("Saving report to %s with data:" % mammo_report_file_path)
    #pprint(desmielinizantes_report_data)
    ReportGenerator.generate_report(out_path=mammo_report_file_path, report=mammo_report_data)

    thorax_report_file_path = path.join(output_dir, "reporte_torax_v4.pdf")
    torax_report_data = ThoraxV4ReportData().get_report_data()
    pprint("Saving report to %s with data:" % thorax_report_file_path)
    #pprint(desmielinizantes_report_data)
    ReportGenerator.generate_report(out_path=thorax_report_file_path, report=torax_report_data)
