import csv
import logging
import copy
import json
from os import path
import pandas as pd
from .base_report_data import ReportData

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NeuroReportData(ReportData):
    TABLE_AREAS = ['TBD']

    # SIDEBAR_MAX_CHARACTERS = 1000

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
        self.header = {}
        # self.header['entelai_img']['absolute_path'] = path.join('..', 'images', 'logo_entelai-neuro.png')
        volumes_file = event['volumes_file'] if 'volumes_file' in event else 'volumes.csv'
        volumes_file_path = path.join(output_dir, volumes_file)

        with open(volumes_file_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            self.data_headers = next(reader)

            self.data_rows = [x for x in reader]
        self.volume_table = self.generate_volume_table()

    def create_reference_row_pilar(self, width, report_label, reference):
        if reference == '':
            label_class, reference_description = 'label label-yellow', 'Moderada'
        elif 'lesions' in reference:
            index = next((i for i, row in enumerate(self.lesions_table) if reference.split('_')[0] in row[0]), 7)
            reference_description = self.lesions_table[index][2]
            if reference_description != '-':
                label_class = 'label label-red'
            else:
                label_class = 'label label-green'
        else:
            label_class, reference_description = self.get_token_info(reference)
        column = {
            'values': [
                {
                    'width': width.__str__() + '%',
                    'value': report_label
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
        return column  # , label,value

    def create_reference_row(self, width, reference, label_class, reference_description):
        column = {
            'values': [
                {
                    'width': width.__str__() + '%',
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

    def create_volumetria_image_column(self, width, reference, image_abs_path, image_class='image-center', style=None):
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

    def generate_table_header(self):
        header = [
            {'value': _('Estructura'), 'style': 'width: 100px'},
            {'value': _('Volumen en cm3'), 'style': 'width: 70px'},
            {'value': _('Volumen en %VIC'), 'style': 'width: 50px'},
            {'value': _('Rango normal ajustado por edad según %VIC'), 'style': 'width: 95px'},
            {'value': _('Percentilo normativo'), 'style': 'width: 80px'},
            {'value': _('Cambio de percentilo'), 'style': 'width: 80px'},
            {'value': _('Tasa de cambio anualizada'), 'style': 'width: 50px'},
        ]

        return header

    def generate_volume_table(self):

        category_order = ['global', 'subcortical', 'ventricular', 'infratentorial', 'cortical']

        entelai_label_idx = self.data_headers.index('entelai_label')
        report_names_idx = self.data_headers.index('report_names')
        volume_idx = self.data_headers.index('volume')
        volume_vic_idx = self.data_headers.index('volume_vic')
        percentile_idx = self.data_headers.index('percentile')
        min_range_idx = self.data_headers.index('min_range')
        max_range_idx = self.data_headers.index('max_range')
        out_of_range_idx = self.data_headers.index('out_of_range')
        category_idx = self.data_headers.index('category')
        percentile_difference_idx = self.data_headers.index('percentile_difference')
        percentile_difference_annual_idx = self.data_headers.index('change_rate_annual')
        significant_difference_idx = self.data_headers.index('difference_significant')
        report_order_idx = self.data_headers.index('report_order')

        rows = []
        for category in category_order:
            # title_row = copy.deepcopy(separation_row)
            # title_row['values'][0]['value'] = category_titles[category]
            printable_rows = []
            for row in self.data_rows:
                if len(row[report_names_idx]) > 0 and len(row[volume_vic_idx]) > 0 and row[category_idx] == category:
                    normative_percentile = row[percentile_idx]
                    if normative_percentile == '1.0':
                        normative_percentile = '< 1'
                    if normative_percentile == '99.0':
                        normative_percentile = '> 99'

                    volume = float(row[volume_vic_idx]) * 100  # Scale to percentage
                    str_volume = '{:1.2f}%'.format(volume)
                    volume_cm3 = float(row[volume_idx]) / 1000
                    if volume_cm3 > 100:
                        str_volume_cm3 = '{:,}'.format(round(volume_cm3))
                    elif volume_cm3 > 10:
                        str_volume_cm3 = '{:1.1f}'.format(volume_cm3)
                    else:
                        str_volume_cm3 = '{:1.2f}'.format(volume_cm3)
                    range_low = max(0, float(row[min_range_idx]) * 100)
                    range_high = float(row[max_range_idx]) * 100
                    str_range = '( {:1.2f} - {:1.2f} )'.format(range_low, range_high)
                    print_name = row[report_names_idx]
                    try:
                        percentile_difference = '{:1.2f} pp'.format(float(row[percentile_difference_idx]))
                        percentile_difference_annual_value = ('{:1.2f}%').format(
                            float(row[percentile_difference_annual_idx]))

                    except (ValueError, KeyError):
                        percentile_difference = '-'
                        percentile_difference_annual_value = '-'
                    percentile_difference_annual = {'style': 'text-align: right; padding-right: 35px', 'items': []}
                    percentile_difference_annual['items'].append(percentile_difference_annual_value)
                    significant_difference = row[significant_difference_idx]

                    ignore_labels_for_arrow = ['left-thalamus-proper*', 'left-caudate', 'left-putamen',
                                               'left-pallidum', 'left-amygdala',
                                               'right-thalamus-proper*', 'right-caudate',
                                               'right-putamen', 'right-pallidum', 'right-amygdala']

                    if row[entelai_label_idx] in ignore_labels_for_arrow:
                        significant_difference_img = {'type': 'image', 'absolute_path': '../images/arrow-empty.png'}
                    else:
                        if significant_difference == 'down':
                            significant_difference_img = {'type': 'image', 'absolute_path': '../images/arrow-down.png'}
                        elif significant_difference == 'up':
                            significant_difference_img = {'type': 'image', 'absolute_path': '../images/arrow-up.png'}
                        else:
                            significant_difference_img = {'type': 'image', 'absolute_path': '../images/arrow-empty.png'}

                    significant_difference_div = {'type': 'div',
                                                  'items': [significant_difference_img]}

                    percentile_difference_annual['items'].append(significant_difference_div)
                    values = [_(print_name), str_volume_cm3, str_volume, str_range, normative_percentile,
                              percentile_difference]  # ,
                    # percentile_difference_annual]
                    if 'true' in row[out_of_range_idx].lower():
                        row = {'style': 'font-weight: bold', 'values': values, 'order': float(row[report_order_idx])}
                    else:
                        row = {'style': '', 'values': values, 'order': float(row[report_order_idx])}
                    printable_rows.append(row)
            # printable_rows = [title_row] + sorted(printable_rows, key=lambda x: x['order'])
            printable_rows = sorted(printable_rows, key=lambda x: x['order'])
            rows = rows + printable_rows
        return rows

    def footer(self, pagenum):
        FOOTER = {
            'type': 'footer',
            'detail': 'Pág {}'.format(pagenum),
        }
        return FOOTER

    def load_sidebar_text(self):
        """ Basic sidebar unless overridden by children"""
        event = self.event
        sidebar = {
            'type': 'sidebar',
            'components': [
                {'type': 'div',
                 'class': 'logo-container',
                 'items': [
                     {
                         'type': 'image',
                         'absolute_path': event['institution_logo'],
                     }
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
                                    'text': self.patient_name,
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
                            'text': self.disclaimer
                        },
                    ]
                }
            ],
        }
        return sidebar

    def get_report_data(self):
        if self.send_error_pdf:
            return self.error_report
        self.sidebar = self.load_sidebar_text()
        report_data = {
            'components': [
                {'type': 'div',
                 'class': 'page',
                 'items':

                     [
                         # self.header,
                         self.sidebar,
                         self.main,
                     ]
                 },
                {
                    'type': 'div',
                    'class': 'page',
                    'items':
                        [
                            # self.header,
                            self.sidebar,
                            self.main2,
                        ]
                },
                {
                    'type': 'div',
                    'class': 'page',
                    'items': [
                        # self.header,
                        self.sidebar,
                        self.get_page3_volume_table(),
                    ]
                }
            ]
        }
        return report_data

    def get_page3_volume_table(self):
        main3 = {
            'type': 'main',
            'components': [
                {'type': 'div',
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
                                 'type': 'subtitle',
                                 'text': 'Áreas Corticales'
                             },
                             {
                                 'type': 'table',
                                 'class': 'striped-table data-table',
                                 'header': self.generate_table_header(),
                                 'rows': self.volume_table[28:]
                             },
                         ],
                     },
                     self.get_instructions(),
                 ]
                 },
                self.footer(3)
            ]
        }

        return main3

    def get_base_page2(self):
        base2 = [
            {
                'type': 'div',
                'items': [
                    {
                        'type': 'title',
                        'text': 'Volumetría',
                    },
                    {
                        'type': 'subtitle',
                        'text': 'Volúmenes Globales',
                    },
                    {
                        'type': 'table',
                        'class': 'striped-table data-table',
                        'header': self.generate_table_header(),
                        'rows': self.generate_volume_table()[1:7],
                    },
                ],
            },
            {
                'type': 'div',
                'class': 'tabla-aireada',
                'items': [
                    {
                        'type': 'subtitle',
                        'text': 'Estructuras Subcorticales'
                    },
                    {
                        'type': 'table',
                        'class': 'striped-table data-table',
                        'header': self.generate_table_header(),
                        'rows': self.generate_volume_table()[8:18]
                    },
                ],
            },
            {
                'type': 'div',
                'class': 'tabla-aireada',
                'items': [
                    {
                        'type': 'subtitle',
                        'text': 'Sistema Ventricular'
                    },
                    {
                        'type': 'table',
                        'class': 'striped-table data-table',
                        'header': self.generate_table_header(),
                        'rows': self.generate_volume_table()[19:21]
                    },
                ],
            },
            {
                'type': 'div',
                'class': 'tabla-aireada',
                'items': [
                    {
                        'type': 'subtitle',
                        'text': 'Estructuras Infratentoriales'
                    },
                    {
                        'type': 'table',
                        'class': 'striped-table data-table',
                        'header': self.generate_table_header(),
                        'rows': self.generate_volume_table()[22:27]
                    },
                ],
            },
        ]

        return base2

    def get_instructions(self):
        footer = {
            'type': 'div',
            'class': 'annotations border-box',
            'items': [
                {
                    'type': 'h3',
                    'text': _('Aclaraciones para el médico')
                },
                {
                    'type': 'paragraph',
                    'text': _('Abreviaturas: VIC (Volume Intracraniano), FPC (Fracción Parenquima Cerebral).')
                },
                {
                    'type': 'paragraph',
                    'class': 'indicaciones-max',
                    'text': _(
                        'Los rangos normales corresponden a los valores contenidos entre el percentil 1% y el 99%. Se destacan con <strong>negrita</strong> las áreas que se encuentren por debajo del límite inferior (superior en el caso del sistema ventricular).')
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

                        _('La disminución anual del volumen de esta área es mayor a la esperada para el rango etario (excepto las estructuras subcorticales).'),
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
                        _('El aumento anual del volumen de esta área es mayor a la esperada para el rango etario (excepto las estructuras subcorticales).'),
                    ],
                },
            ],

        }

        return footer

    def get_token_info(self, volume_label):
        volume_table = pd.read_csv(path.join(self.output_dir, 'volumes.csv'))

        percentile = float(volume_table.loc[volume_table['entelai_label'] == volume_label, 'percentile'].values[0])
        # label_name = volume_table.loc[volume_table['entelai_label']==volume_label, 'report_names'].values[0]
        if percentile < 1:
            value = _('Percentilo <1%')
            color_label = 'label label-red'
        elif percentile < 5:

            value = _('Percentilo <5%')
            color_label = 'label label-yellow'
        else:
            value = _('Normal')
            color_label = 'label label-green'

        return color_label, value

    def atrophy_indications(self):
        atrophy = {
            'type': 'div',
            'class': 'description',
            'items': [
                {
                    'type': 'span',
                    'class': 'swatch teal-bg'
                },
                {
                    'type': 'h3',
                    'text': 'Percentilo < 5%',
                },
                {
                    'type': 'span',
                    'class': 'swatch red-bg'
                },
                {
                    'type': 'h3',
                    'text': 'Percentilo < 1%',
                },
            ],
        }
        return atrophy


class VolumetriaReportData(NeuroReportData):

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
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
                                    'text': _('Principales hallazgos de volumetría'),
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
                                                            self.create_reference_row(75, _('Calidad de Imagen'),
                                                                                      'label label-yellow',
                                                                                      _('Moderada')),
                                                            self.create_reference_row(75, _('Volúmen cerebro (FPC)'),
                                                                                      'label label-green', _('Baja')),
                                                            self.create_reference_row(75, _('Corteza frontal'),
                                                                                      'label label-green', _('Baja')),
                                                            self.create_reference_row(75, _('Corteza temporal'),
                                                                                      'label label-green', _('Baja')),
                                                            self.create_reference_row(75, _('Corteza parietal'),
                                                                                      'label label-teal', _('Minima')),
                                                            self.create_reference_row(75, _('Corteza occipital'),
                                                                                      'label label-green', _('Baja')),
                                                            self.create_reference_row(75, _('Ventrículos'),
                                                                                      'label label-teal', _('Minima')),
                                                            self.create_reference_row(75, _('Tronco encefálico'),
                                                                                      'label label-red', _('Alta')),
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
                                                            self.create_reference_row(75, _('Hipocampo izquierdo'),
                                                                                      'label label-yellow',
                                                                                      _('Moderada')),
                                                            self.create_reference_row(75, _('Hipocampo derecho'),
                                                                                      'label label-green', _('Baja')),
                                                            self.create_reference_row(75,
                                                                                      _('Asimetría hipocampal (AIH)'),
                                                                                      'label label-green', _('Baja')),
                                                            self.create_reference_row(75, _('Corteza parahipocampal'),
                                                                                      'label label-green', _('Baja')),
                                                            # LOS DOS TODO
                                                            self.create_reference_row(75, _('Corteza entorrinal'),
                                                                                      'label label-teal', _('Minima')),
                                                            # LOS DOS
                                                            self.create_reference_row(75,
                                                                                      _('Corteza parietal inferior'),
                                                                                      'label label-green', _('Baja')),
                                                            # LOS DOS
                                                            self.create_reference_row(75, _('Precúneo'),
                                                                                      'label label-teal', _('Minima')),
                                                            # LOS DOS!!!
                                                            self.create_reference_row(75, _('Cúneo'), 'label label-red',
                                                                                      _('Alta')),  # los dos!!
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
                                                self.create_volumetria_image_column(33, _('Volumen cerebro (FPC)'),
                                                                                    path.join(output_dir, 'bpf.png'), ),
                                                self.create_volumetria_image_column(33, _('Sustancia blanca'),
                                                                                    path.join(output_dir, 'wm.png')),
                                                self.create_volumetria_image_column(33, _('Sustancia gris total'),
                                                                                    path.join(output_dir, 'gm.png')),
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
                                                self.create_volumetria_image_column(33, _('Sustancia Gris Cortical'),
                                                                                    '../images/img1.jpg'),
                                                self.create_volumetria_image_column(33, _('Hipocampo Derecho'),
                                                                                    path.join(output_dir,
                                                                                              'right-hippocampus.png')),
                                                self.create_volumetria_image_column(33, _('Hipocampo Izquierdo'),
                                                                                    path.join(output_dir,
                                                                                              'left-hippocampus.png')),
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
                                                                                    path.join(output_dir,
                                                                                              'supratentorial_ventricles.png')),
                                                self.create_volumetria_image_column(33, _('Asimetría Hipocampal'),
                                                                                    '../images/img2.jpg'),
                                                self.create_volumetria_image_column(33, _('Volúmen Corteza'),
                                                                                    path.join(output_dir,
                                                                                              'radial.png')),
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
                                    'text': 'Reconstrucción 3D de Cerebro',
                                },
                                {
                                    'type': 'table',
                                    'rows': [
                                        {
                                            'values': [
                                                self.create_volumetria_image_column(33, _('Carga lesional'),
                                                                                    path.join(output_dir,
                                                                                              '3Dview_subctx.png'),
                                                                                    'image-center',
                                                                                    ';padding-right: 10px'),
                                                self.create_volumetria_image_column(33, _('Volumetría Subcortical'),
                                                                                    path.join(output_dir,
                                                                                              '3Dview_subctx.png'),
                                                                                    'image-center',
                                                                                    ';padding-right: 10px'),
                                                self.create_volumetria_image_column(33, _('Volumetría Cortical'),
                                                                                    path.join(output_dir,
                                                                                              '3Dview_ctx1.png'),
                                                                                    'image-center',
                                                                                    ';padding-right: 10px'),
                                            ]
                                        }
                                    ]
                                },
                                self.atrophy_indications()
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
                {'type': 'div',
                 'class': 'content',
                 'items': self.get_base_page2(),
                 },
                self.footer(2),
            ]
        }


class DesmielinizantesReportData(NeuroReportData):

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
        self.lesions_table = self.get_lesion_rows()
        logger.info('cambios pdf nuevos ')
        self.main = {
            'type': 'main',
            'components': [
                {'type': 'div',
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
                                 'text': _('Principales hallazgos'),
                                 'type': 'paragraph',
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
                                                         self.create_reference_row(75, _('Calidad de Imagen'),
                                                                                   'label label-yellow', _('Moderada')),
                                                         self.create_reference_row(75, _('Volúmen Cerebro (FPC)'),
                                                                                   'label label-green', _('Baja')),
                                                         self.create_reference_row(75, _('Sustancia Blanca'),
                                                                                   'label label-green', _('Baja')),
                                                         self.create_reference_row(75, _('Sustancia Gris'),
                                                                                   'label label-green', _('Baja')),
                                                         self.create_reference_row(75, _('Cerebelo'),
                                                                                   'label label-teal', _('Minima')),
                                                         self.create_reference_row(75, _('Tronco Encefálico'),
                                                                                   'label label-green', _('Baja')),
                                                         self.create_reference_row(75, _('Tálamo Izquierdo'),
                                                                                   'label label-teal', _('Minima')),
                                                         self.create_reference_row(75, _('Tálamo Derecho'),
                                                                                   'label label-red', _('Alta')),
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
                                                     'style': 'padding-left: 10px;',
                                                     'rows': [
                                                         self.create_reference_row(75, _('Carga Lesional (Percentilo)'),
                                                                                   'label label-yellow', _('Moderada')),
                                                         # baja moderada alta
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
                                                         self.create_reference_row(75, _('Lesiones Estables'),
                                                                                   'label label-teal', _('Minima')),
                                                         # numeros con color estandar
                                                         self.create_reference_row(75, _('Lesiones Crecientes'),
                                                                                   'label label-green', _('Baja')),
                                                         self.create_reference_row(75, _('Nuevas Lesiones'),
                                                                                   'label label-teal', _('Minima')),
                                                         # rojo si mas de una poner numero
                                                         self.create_reference_row(75, _('Carga Lesional Total'),
                                                                                   'label label-red', _('Alta')),
                                                     ]
                                                 }
                                             ]
                                         },
                                     ]
                                     },
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
                                             self.create_volumetria_image_column(33, _('Volumen Cerebro (FPC)'),
                                                                                 path.join(output_dir, 'bpf.png')),
                                             self.create_volumetria_image_column(33, _('Sustancia Blanca'),
                                                                                 path.join(output_dir, 'wm.png')),
                                             self.create_volumetria_image_column(33, _('Sustancia Gris'),
                                                                                 path.join(output_dir, 'gm.png')),
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
                                             self.create_volumetria_image_column(33, _('Tálamo Izquierdo'),
                                                                                 path.join(output_dir,
                                                                                           'left-thalamus-proper*.png')),
                                             self.create_volumetria_image_column(33, _('Tálamo Derecho'),
                                                                                 path.join(output_dir,
                                                                                           'right-thalamus-proper*.png')),
                                             self.create_volumetria_image_column(33, _('Ventrículos'),
                                                                                 path.join(output_dir,
                                                                                           'supratentorial_ventricles.png')),
                                         ]
                                     }
                                 ]
                             }
                         ]
                     },
                     {
                         'type': 'div',
                         'items': [
                             {
                                 'type': 'table',
                                 'rows': [
                                     {
                                         'values': [
                                             self.create_volumetria_image_column(33, _('Cerebelo'),
                                                                                 path.join(output_dir,
                                                                                           'cerebellum.png')),
                                             self.create_volumetria_image_column(33, _('Tronco Encefálico'),
                                                                                 path.join(output_dir,
                                                                                           'brain-stem.png')),
                                             self.create_volumetria_image_column(33, _('Volúmen Corteza'),
                                                                                 path.join(output_dir, 'radial.png')),
                                         ]
                                     }
                                 ]
                             }
                         ]
                     },
                     {
                         'type': 'div',
                         'items': [
                             {
                                 'type': 'title',
                                 'text': 'Reconstrucción 3D de Cerebro',
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
                             self.atrophy_indications()
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
                {'type': 'div',
                 'class': 'content',
                 'items': self.get_base_page2(),
                 },
                self.footer(2),
            ]
        }

    def get_lesion_rows(self):
        label_idx = self.data_headers.index('entelai_label')
        volume_idx = self.data_headers.index('volume')
        value_idx = self.data_headers.index('value')
        volume_vic_idx = self.data_headers.index('volume_vic')
        significant_difference_idx = self.data_headers.index('difference_significant')
        try:
            previous_volume_idx = self.data_headers.index('previous_volume')
            previous_value_idx = self.data_headers.index('previous_value')
            previous_volume_vic_idx = self.data_headers.index('previous_volume_vic')
        except ValueError:
            previous_volume_idx = None
            previous_volume_vic_idx = None

        printable_rows = []
        lesion_volume = None
        lesion_volume_vic = None
        previous_lesion_volume = None
        previous_lesion_count = None
        previous_lesion_volume_vic = None
        active_volume = None
        active_volume_vic = None
        stable_lesions_count = None
        new_lesions_count = None
        grow_lesions_count = None

        for row in self.data_rows:
            if row[label_idx] == 'lesions':
                try:
                    significant_difference = row[significant_difference_idx]
                    if significant_difference == 'down':
                        significant_difference_img = {'type': 'image', 'absolute_path': '../images/arrow-down.png'}
                    elif significant_difference == 'up':
                        significant_difference_img = {'type': 'image', 'absolute_path': '../images/arrow-up.png'}
                    else:
                        significant_difference_img = None

                    significant_difference_div = {'type': 'div',
                                                  'items': [significant_difference_img]}

                    lesion_volume_value = '<strong>{:1.2f}</strong>'.format(float(row[volume_idx]) / 1000.0)
                    lesion_volume = {'style': '', 'items': []}
                    lesion_volume['items'].append(lesion_volume_value)
                    if significant_difference_img:
                        lesion_volume['items'].append(significant_difference_div)
                    lesion_count = int(float(row[value_idx]))
                    lesion_volume_vic = '<strong>{:1.2f} %</strong>'.format(float(row[volume_vic_idx]) * 100)
                except ValueError as e:
                    lesion_volume = '-'
                    lesion_count = 0
                    lesion_volume_vic = '-'
                    logger.exception(e)

                if previous_volume_idx and previous_value_idx and previous_volume_vic_idx:
                    try:
                        previous_lesion_volume = '{:1.2f}'.format(float(row[previous_volume_idx]) / 1000)
                        previous_lesion_count = '{:d}'.format(int(float(row[previous_value_idx])))
                        previous_lesion_volume_vic = '{:1.2f} %'.format(float(row[previous_volume_vic_idx]) * 100)
                    except ValueError:
                        previous_lesion_volume = '-'
                        previous_lesion_count = '-'
                        previous_lesion_volume_vic = '-'
                else:
                    previous_lesion_volume = '-'
                    previous_lesion_volume_vic = '-'

            if row[label_idx] == 'active_lesions':
                try:
                    active_volume = '{:1.2f}'.format(float(row[volume_idx]) / 1000)
                    active_volume_vic = '{:1.2f} %'.format(float(row[volume_vic_idx]) * 100)
                except ValueError:
                    active_volume = '-'
                    active_volume_vic = '-'

            if row[label_idx] == 'lesions_longitudinal_stable':
                try:
                    stable_lesions_count = int(float(row[value_idx]))
                except ValueError:
                    stable_lesions_count = None
            if row[label_idx] == 'lesions_longitudinal_grow':
                try:
                    grow_lesions_count = int(float(row[value_idx]))
                except ValueError:
                    grow_lesions_count = None
            if row[label_idx] == 'lesions_longitudinal_new':
                try:
                    new_lesions_count = int(float(row[value_idx]))
                except ValueError:
                    new_lesions_count = None
        if not lesion_volume:
            lesion_volume = '-'
            lesion_count = '-'
            lesion_volume_vic = '-'

        if not previous_lesion_volume:
            previous_lesion_volume = '-'
            previous_lesion_volume_vic = '-'

        if not previous_lesion_count:
            previous_lesion_count = '-'

        if not active_volume:
            active_volume = '-'
            active_volume_vic = '-'

        stable_lesions_count_str = '<strong>{:d}</strong>'.format(
            stable_lesions_count) if stable_lesions_count is not None else '-'
        grow_lesions_count_str = '<strong>{:d}</strong>'.format(
            grow_lesions_count) if grow_lesions_count is not None else '-'
        new_lesions_count_str = '<strong>{:d}</strong>'.format(
            new_lesions_count) if new_lesions_count is not None else '-'

        lesion_count_long = sum(
            num for num in [stable_lesions_count, grow_lesions_count, new_lesions_count] if num is not None)
        lesion_count_str = '<strong>{:d}</strong>'.format(
            lesion_count_long) if lesion_count_long > 0 else '<strong>{:d}</strong>'.format(lesion_count)

        rows = [
            [_('Hiperintensas en FLAIR (cm3)'), previous_lesion_volume, lesion_volume],
            [_('Hiperintensas en FLAIR (%VIC)'), previous_lesion_volume_vic, lesion_volume_vic],
            # ['Gadolinio positivas (cm3)', active_volume, '-'], #  Not showing for now.
            # ['Gadolinio positivas (%VIC)', active_volume_vic, '-']
            [_('Número de lesiones totales (&#8805; 3mm de diámetro)'), previous_lesion_count, lesion_count_str],
            [_('&nbsp;&nbsp;<em>Lesiones estables/decrecientes</em>'), '-', stable_lesions_count_str],
            [_('&nbsp;&nbsp;<em>Lesiones crecientes</em>'), '-', grow_lesions_count_str],
            [_('&nbsp;&nbsp;<em>Lesiones nuevas</em>'), '-', new_lesions_count_str],
        ]
        return rows