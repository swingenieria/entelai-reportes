import csv
import logging
import copy
import json
from os import path
from .base_report_data import ReportData

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class NeuroReportData(ReportData):
    TABLE_AREAS = ['TBD']
    SIDEBAR_MAX_CHARACTERS = 1000

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
        self.header['entelai_img']['absolute_path'] = path.join('..', 'images', 'logo_entelai-neuro.png')
        volumes_file = event['volumes_file'] if 'volumes_file' in event else 'volumes.csv'
        volumes_file_path = path.join(output_dir, volumes_file)
        self.areas_table_header = [_('Estructura'), _('Volumen en cm3'),_('Volumen en %VIC'),
                                   _('Rango normal ajustado por edad según %VIC'),
                                   _('Percentilo normativo'), _('Cambio de percentilo'),
                                   _('Tasa de cambio anualizada')]
        self.config = json.loads(event['config'])
        if 'hide_3D_volumes' in self.config and self.config['hide_3D_volumes']:
            self.volumes_3D_table = []
        else:
            self.volumes_3D_table = [
                {
                    'type': 'table',
                    'class': 'images-with-titles only-title',
                    'rows': [
                        [_('Mapa de calor de volumen según área')]
                    ]
                }, {
                    'type': 'table',
                    'class': 'images-with-titles',
                    'rows': [
                        [{'type': 'image', 'width': '15%',
                          'absolute_path': path.join(output_dir, '3Dview_subctx.png')},
                         {'type': 'image', 'width': '15%',
                          'absolute_path': path.join(output_dir, '3Dview_ctx2.png')},
                         {'type': 'image', 'width': '15%',
                          'absolute_path': path.join(output_dir, '3Dview_ctx1.png')},
                         ],
                    ]
                }, {
                    'type': 'table',
                    'rows': [[{'type': 'reference', 'color': '#44B9D9', 'text': _('Área a revisar')},
                              {'type': 'reference', 'color': '#db630d', 'text': _('Área posiblemente atrófica')}]]
                }]

        with open(volumes_file_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            self.data_headers = next(reader)
            self.data_rows = [x for x in reader]
    
    @staticmethod
    def instructions():
        return {
                    'type': 'div',
                    'class': 'bg-color2',
                    'items': [
                        {
                            'type': 'paragraph',
                            'text': '<strong>' + _('Aclaraciones para el médico') + '</strong>'
                        },
                        {
                            'type': 'paragraph',
                            'text': _('Abreviaturas: VIC (Volumen Intracraneal)')
                        },
                        {
                            'type': 'paragraph',
                            'text': _('Los rangos normales corresponden a los valores contenidos entre el percentil 1% y el 99%. Se destacan con <strong>negrita</strong> las áreas que se encuentren por debajo del límite inferior (superior en el caso del sistema ventricular).')
                        },
                        {
                            'type': 'div',
                            'class': 'izquierda2',
                            'items': [
                                {
                                    'type': 'image',
                                    'absolute_path': '../images/arrow-down.png',
                                    'class': 'flotante'
                                },
                                {
                                    'type': 'paragraph',
                                    'text': _('La disminución anual del volumen de esta área es mayor a la esperada para el rango etario (excepto las estructuras subcorticales)')
                                }
                            ]
                        },
                        {
                            'type': 'div',
                            'class': 'izquierda2',
                            'items': [
                                {
                                    'type': 'image',
                                    'absolute_path': '../images/arrow-up.png',
                                    'class': 'flotante'
                                },
                                {
                                    'type': 'paragraph',
                                    'text': _('El aumento anual del volumen de esta área es mayor a la esperada para el rango etario (excepto las estructuras subcorticales)')
                                }
                            ]
                        },
                    ]
                }

    def generate_volume_table(self):
        separation_row = {
            'class': 'bg-color',
            'values': [
                {
                    'colspan': '7',
                    'value': 'VOLÚMENES GLOBALES'
                }
            ]
        }
        category_order = ['global', 'subcortical', 'ventricular', 'infratentorial', 'cortical']
        category_titles = {'global': _('VOLÚMENES GLOBALES'),
                           'subcortical': _('ESTR. SUBCORTICALES'),
                           'ventricular': _('SISTEMA VENTRICULAR'),
                           'infratentorial': _('ESTR. INFRATENTORIALES'),
                           'cortical': _('ÁREAS CORTICALES')
        }
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
            title_row = copy.deepcopy(separation_row)
            title_row['values'][0]['value'] = category_titles[category]
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
                    volume_cm3 = float(row[volume_idx])/1000
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
                        percentile_difference_annual_value = ('{:1.2f}%').format(float(row[percentile_difference_annual_idx]))
                        
                    except (ValueError, KeyError):
                        percentile_difference = '-'
                        percentile_difference_annual_value = '-'
                    percentile_difference_annual = {'style': 'text-align: right; padding-right: 35px','items': []}
                    percentile_difference_annual['items'].append(percentile_difference_annual_value)
                    significant_difference = row[significant_difference_idx]

                    ignore_labels_for_arrow = ['left-thalamus-proper*', 'left-caudate', 'left-putamen', 
                        'left-pallidum', 'left-amygdala',
                        'right-thalamus-proper*', 'right-caudate',
                        'right-putamen','right-pallidum','right-amygdala']

                    if row[entelai_label_idx] in ignore_labels_for_arrow:
                        significant_difference_img = {'type': 'image', 'class': 'arrow', 'absolute_path': '../images/arrow-empty.png'}
                    else:
                        if significant_difference == 'down':
                            significant_difference_img = {'type': 'image', 'class': 'arrow', 'absolute_path': '../images/arrow-down.png'}
                        elif significant_difference == 'up':
                            significant_difference_img = {'type': 'image', 'class': 'arrow', 'absolute_path': '../images/arrow-up.png'}
                        else: 
                            significant_difference_img = {'type': 'image', 'class': 'arrow', 'absolute_path': '../images/arrow-empty.png'}
                    
                    significant_difference_div = {'type': 'div', 'class': 'izquierda',
                                                    'items': [significant_difference_img]}
                    
                    percentile_difference_annual['items'].append(significant_difference_div)
                    values = [_(print_name),str_volume_cm3, str_volume, str_range, normative_percentile, percentile_difference,
                              percentile_difference_annual]
                    if 'true' in row[out_of_range_idx].lower():
                        row = {'style': 'font-weight: bold', 'values': values, 'order': float(row[report_order_idx]) }
                    else:
                        row = {'style': '', 'values': values, 'order': float(row[report_order_idx])}
                    printable_rows.append(row)
            printable_rows = [title_row] + sorted(printable_rows, key=lambda x: x['order'])
            rows = rows + printable_rows
        return rows

    def _set_sidebar_font(self):
        filtered_finding_labels = {x: self.findings[x] for x in self.findings if x not in {'send_error_pdf'}}
        total_chars = len(self.sidebar_intro) + sum([len(' '.join(phrases)) for phrases in filtered_finding_labels.values()])
        logger.info(f'Total chars in sidebar is {total_chars}')
        if total_chars > self.SIDEBAR_MAX_CHARACTERS:
            logger.info('Total chars: {} exceeds MAXIMUM, using smaller font'.format(total_chars))
            for component in self.sidebar['components']:
                component['class'] = 'small-font'

    def load_sidebar_text(self):
        """ Basic sidebar unless overridden by children"""
        sidebar = {
            'type': 'sidebar',
            'components': [{
                            'type': 'title',
                            'text': _('Reporte de análisis automatizado por inteligencia artificial')
                            }, {
                            'type': 'paragraph',
                            'text': _('''Este estudio se analizó utilizando un sistema de inteligencia artificial. Se
                                       presentan los resultados de la cuantificación volumétrica para la
                                       revisión por el especialista.''')
                           }]}
        return sidebar

    def get_report_data(self):
        if self.send_error_pdf:
            return self.error_report
        self.sidebar = self.load_sidebar_text()
        self._set_sidebar_font()
        report_data = {
            'components': [{
                'type': 'page',
                'class': self.institution_logo_class,
                'components': [
                    self.header,
                    self.sidebar,
                    self.main,
                    self.footer(1)
                ]
            }, {
                'type': 'page',
                'class': self.institution_logo_class,
                'components': [
                    self.header,
                    self.main2,
                    self.footer(2)
                ]
            }, {
                'type': 'page',
                'class': self.institution_logo_class,
                'components': [
                    self.header,
                    self.main3,
                    self.footer(3)
                ]
            }

            ]
        }
        return report_data


class VolumetriaReportData(NeuroReportData):

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
        self.main = {
            'type': 'main',
            'components': [
                              {
                                  'type': 'table',
                                  'class': 'images-with-titles',
                                  'rows': [
                                      [_('Volumen cerebro (FPC)'),
                                       {'style': 'width: 8%; background-color: white;', 'value': ''},
                                       _('Volumen sustancia gris cortical')],
                                      [{'type': 'image', 'absolute_path': path.join(output_dir, 'bpf.png'),
                                        'style': 'width:100%;'},
                                       {'style': 'width: 8%; background-color: white;', 'value': ''},
                                       {'type': 'image', 'absolute_path': path.join(output_dir, 'gm.png'),
                                        'style': 'width:100%;'}],
                                      [_('Volumen hipocampo izquierdo'),
                                       {'style': 'width: 4%; background-color: white;', 'value': ''},
                                       _('Volumen hipocampo derecho')],
                                      [{'type': 'image', 'absolute_path': path.join(output_dir, 'left-hippocampus.png'),
                                        'style': 'width:100%;'},
                                       {'style': 'width: 8%; background-color: white;', 'value': ''},
                                       {'type': 'image', 'absolute_path': path.join(output_dir, 'right-hippocampus.png'),
                                        'style': 'width:100%;'}],
                                      [_('Volumen corteza'),
                                       {'style': 'width: 4%; background-color: white;', 'value': ''},
                                       _('Volumen ventrículos')],
                                      [{'type': 'image', 'absolute_path': path.join(output_dir, 'radial.png'),
                                        'style': 'width:90%; margin-left:5%'},
                                       {'style': 'width: 8%; background-color: white;', 'value': ''},
                                       {'type': 'image', 'absolute_path': path.join(output_dir, 'supratentorial_ventricles.png'),
                                        'style': 'width:100%; margin-top:5%'}],
                                  ]
                              },
                              {
                                  'type': 'table',
                                  'class': 'images-with-titles only-title',
                                  'rows': [
                                      [_('Segmentación de tejidos y áreas')]
                                  ]
                              },
                              {
                                  'type': 'table',
                                  'class': 'images-with-titles',
                                  'rows': [
                                      [{'type': 'image',
                                        'absolute_path': path.join(output_dir, 'slices_tissue_0.png')},
                                       {'type': 'image',
                                        'absolute_path': path.join(output_dir, 'slices_tissue_1.png')},
                                       {'type': 'image',
                                        'absolute_path': path.join(output_dir, 'slices_tissue_2.png')}],
                                  ]
                              },
                          ] + self.volumes_3D_table
        }

        self.main2 = {
            'type': 'main',
            'components': [
                {
                    'type': 'title',
                    'text': _('Volumen según estructuras')
                },
                {
                    'type': 'table',
                    'class': 'data-table areas',
                    'header': self.areas_table_header,
                    'rows': self.generate_volume_table()[:27]
                }
            ]
        }

        self.main3 = {
            'type': 'main',
            'components': [
                {
                    'type': 'title',
                    'text': _('Volumen según estructuras')
                },
                {
                    'type': 'table',
                    'class': 'data-table areas',
                    'header': self.areas_table_header,
                    'rows': self.generate_volume_table()[27:]
                },
                self.instructions()
            ]
        }

    def load_sidebar_text(self):
        if 'hide_sidebar_text' in self.config and self.config['hide_sidebar_text']:
            return super().load_sidebar_text()
        sidebar = {
            'type': 'sidebar',
            'components': [{
                'type': 'paragraph',
                'text': self.sidebar_intro
            }, {
                'type': 'title',
                'text': _('VOLUMETRÍA')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['bpf']) + '<br/>' + self.findings['subcortical']
            }, {
                'type': 'title',
                'text': _('HIPOCAMPOS')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['hippo'])
            }, {
                'type': 'title',
                'text': _('SISTEMA VENTRICULAR')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['ventricles'])
            }, {
                'type': 'title',
                'text': _('TRONCO ENCEFÁLICO')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['stem'])
            }]
        }
        return sidebar


class DesmielinizantesReportData(NeuroReportData):

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
        self.main = {
            'type': 'main',
            'components': [
                              {
                                  'type': 'table',
                                  'class': 'images-with-titles',
                                  'rows': [
                                      [_('Volumen cerebro (FPC)'),
                                       {'style': 'width: 8%; background-color: white;', 'value': ''},
                                       _('Volumen sustancia gris cortical')],
                                      [{'type': 'image', 'absolute_path': path.join(output_dir, 'bpf.png'),
                                        'style': 'width:100%;'},
                                       {'style': 'width: 8%; background-color: white;', 'value': ''},
                                       {'type': 'image', 'absolute_path': path.join(output_dir, 'gm.png'),
                                        'style': 'width:100%'}]
                                  ]
                              }, {
                    'type': 'br'
                }, {
                    'type': 'table',
                    'class': 'images-with-titles only-title',
                    'rows': [
                        [_('Segmentación de tejidos y áreas')]
                    ]
                },
                              {
                                  'type': 'table',
                                  'class': 'images-with-titles',
                                  'rows': [
                                      [{'type': 'image', 'width': '15%',
                                        'absolute_path': path.join(output_dir, 'slices_tissue_0.png'),
                                        },
                                       {'type': 'image', 'width': '15%',
                                        'absolute_path': path.join(output_dir, 'slices_tissue_1.png'),
                                        },
                                       {'type': 'image', 'width': '15%',
                                        'absolute_path': path.join(output_dir, 'slices_tissue_2.png'),
                                        }],
                                  ]
                              }, {
                    'type': 'br'
                }, {
                    'type': 'table',
                    'class': 'images-with-titles only-title',
                    'rows': [
                        [_('Lesiones hiperintensas FLAIR')]
                    ]
                }, {
                    'type': 'table',
                    'class': 'images-with-titles',
                    'rows': [
                        [{'type': 'image', 'width': '15%',
                          'absolute_path': path.join(output_dir, 'slices_lesion_0.png')},
                         {'type': 'image', 'width': '15%',
                          'absolute_path': path.join(output_dir, 'slices_lesion_1.png')},
                         {'type': 'image', 'width': '15%',
                          'absolute_path': path.join(output_dir, 'slices_lesion_2.png')}],
                    ]
                }, {
                    'type': 'table',
                    'rows': [[{'type': 'reference', 'color': '#EDCB21', 'text': _('Lesiones estables/decrecientes')},
                              {'type': 'reference', 'color': '#FF0000', 'text': _('Lesiones crecientes')},
                              {'type': 'reference', 'color': '#FF0000', 'text': _('Lesiones nuevas')}]],
                }, {
                    'type': 'br'
                }, {
                    'type': 'br'
                },

                          ] + self.volumes_3D_table
        }

        self.main2 = {
            'type': 'main',
            'components': [
                {
                    'type': 'title',
                    'text': _('Análisis volumétrico de lesiones')
                },
                {
                    'type': 'table',
                    'class': 'data-table',
                    'header': [_('Cuantificación de lesiones hiperintensas en FLAIR'), _('Estudio anterior'), _('<strong>Estudio actual</strong>')],
                    'rows': self.get_lesion_rows()
                },
                {
                    'type': 'title',
                    'text': _('Volumen según estructuras')
                },
                {
                    'type': 'table',
                    'class': 'data-table areas',
                    'header': self.areas_table_header,
                    'rows': self.generate_volume_table()[:23]
                }
            ]
        }

        self.main3 = {
            'type': 'main',
            'components': [
                {
                    'type': 'title',
                    'text': _('Volumen según estructuras')
                },
                {
                    'type': 'table',
                    'class': 'data-table areas',
                    'header': self.areas_table_header,
                    'rows': self.generate_volume_table()[23:]
                },
                self.instructions()
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
                        significant_difference_img = {'type': 'image', 'class': 'arrow', 'absolute_path': '../images/arrow-down.png'}
                    elif significant_difference == 'up':
                        significant_difference_img = {'type': 'image', 'class': 'arrow', 'absolute_path': '../images/arrow-up.png'}
                    else: 
                        significant_difference_img = None
                    
                    significant_difference_div = {'type': 'div', 'class': 'izquierda',
                                                    'items': [significant_difference_img]}

                    lesion_volume_value = '<strong>{:1.2f}</strong>'.format(float(row[volume_idx]) / 1000.0)
                    lesion_volume = {'style': '','items': []}
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
        
        if stable_lesions_count is not None and grow_lesions_count is not None and new_lesions_count is not None:
            lesion_count_str = '<strong>{:d}</strong>'.format(stable_lesions_count + grow_lesions_count+new_lesions_count)
            stable_lesions_count_str = '<strong>{:d}</strong>'.format(stable_lesions_count)
            grow_lesions_count_str = '<strong>{:d}</strong>'.format(grow_lesions_count)
            new_lesions_count_str = '<strong>{:d}</strong>'.format(new_lesions_count)
        else:
            lesion_count_str = '<strong>{:d}</strong>'.format(lesion_count)
            stable_lesions_count_str = '-'
            grow_lesions_count_str = '-'
        

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

    def load_sidebar_text(self):
        if 'hide_sidebar_text' in self.config and self.config['hide_sidebar_text']:
            return super().load_sidebar_text()
        sidebar = {
            'type': 'sidebar',
            'components': [{
                'type': 'paragraph',
                'text': self.sidebar_intro
            },
                {
                    'type': 'title',
                    'text': _('DETECCIÓN DE LESIONES')
                }, {
                    'type': 'paragraph',
                    'text': ' '.join(self.findings['lesions'])
                }, {
                'type': 'title',
                'text': _('VOLUMETRÍA')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['bpf']) + '<br/>' + self.findings['subcortical']
            }, {
                'type': 'title',
                'text': _('HIPOCAMPOS')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['hippo'])
            }, {
                'type': 'title',
                'text': _('SISTEMA VENTRICULAR')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['ventricles'])
            }, {
                'type': 'title',
                'text': _('TRONCO ENCEFÁLICO')
            }, {
                'type': 'paragraph',
                'text': ' '.join(self.findings['stem'])
            }]
        }
        return sidebar
