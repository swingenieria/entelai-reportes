import logging
import os
from os import path
from .base_report_data import ReportData
import pickle

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MammoReportData(ReportData):

    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)

        if 'mammo' in self.config:
            self.config = self.config['mammo']
        self.hide_heatmaps = \
            True if (('hide_heatmaps' in self.config) and self.config['hide_heatmaps']) else False

        self.header['entelai_img']['absolute_path'] = path.join('..', 'images', 'logo-rosa.png')
        self.main = self.load_main_section()
        self.sidebar = self.load_sidebar()
        self.header['table'] = {
            'rows': [
                [_('Paciente'), _('ID de Paciente'), _('Nombre del estudio'), _('Fecha del estudio')],
                [self.patient_name, self.patient_id, self.study_name, self.study_date],
                [_('Edad'), _('Género')],
                [self.age, self.gender]
            ]
        }
        self.disclaimer = _("Producto médico autorizado por ANMAT e inscripto en el Registro Nacional de "
                            "Productores y Productos de Tecnología Médica (bajo el número 2477-1) y ANVISA "
                            "(número de registro 80102512470). Versión {}")

    def load_main_section(self):
        first_image_path = path.join(self.output_dir, 'best_crop-L-CC.png')
        if path.isfile(first_image_path):
            if self.hide_heatmaps:
                first_view = [
                    [_('Izquierda - CC')],
                    [{'type': 'image', 'absolute_path': first_image_path, 'style': 'width:200px; height:152px'}]]
            else:
                first_image_path_heatmap = path.join(self.output_dir, 'heatmap_overlay_contour-L-CC.png')
                first_view = [
                    [_('Izquierda - CC'),
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     _('Izquierda - CC')],
                    [{'type': 'image', 'absolute_path': first_image_path,
                      'style': 'width:200px; height:152px'},
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     {'type': 'image', 'absolute_path': first_image_path_heatmap,
                      'style': 'width:200px; height:152px'}]]
        else:
            first_view = [[]]

        second_image_path = path.join(self.output_dir, 'best_crop-L-MLO.png')
        if path.isfile(second_image_path):
            if self.hide_heatmaps:
                second_view = [
                    [_('Izquierda - MLO')],
                    [{'type': 'image', 'absolute_path': second_image_path, 'style': 'width:200px; height:152px'}]]
            else:
                second_image_path_heatmap = path.join(self.output_dir, 'heatmap_overlay_contour-L-MLO.png')
                second_view = [
                    [_('Izquierda - MLO'),
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     _('Izquierda - MLO')],
                    [{'type': 'image', 'absolute_path': second_image_path,
                      'style': 'width:200px; height:152px'},
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     {'type': 'image', 'absolute_path': second_image_path_heatmap,
                      'style': 'width:200px; height:152px'}]]
        else:
            second_view = [[]]

        third_image_path = path.join(self.output_dir, 'best_crop-R-CC.png')
        if path.isfile(third_image_path):
            if self.hide_heatmaps:
                third_view = [
                    [_('Derecha - CC')],
                    [{'type': 'image', 'absolute_path': third_image_path, 'style': 'width:200px; height:152px'}]]
            else:
                third_image_path_heatmap = path.join(self.output_dir, 'heatmap_overlay_contour-R-CC.png')
                third_view = [
                    [_('Derecha - CC'),
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     _('Derecha - CC')],
                    [{'type': 'image', 'absolute_path': third_image_path,
                     'style': 'width:200px; height:152px'},
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     {'type': 'image', 'absolute_path': third_image_path_heatmap,
                     'style': 'width:200px; height:152px'}]]
        else:
            third_view = [[]]

        fourth_image_path = path.join(self.output_dir, 'best_crop-R-MLO.png')
        if path.isfile(fourth_image_path):
            if self.hide_heatmaps:
                fourth_view = [
                    [_('Derecha - MLO')],
                    [{'type': 'image', 'absolute_path': third_image_path, 'style': 'width:200px; height:152px'}]]
            else:
                fourth_image_path_heatmap = path.join(self.output_dir, 'heatmap_overlay_contour-R-MLO.png')
                fourth_view = [
                    [_('Derecha - MLO'),
                     {'style': 'width: 4%; background-color: white;',
                     'value': ''}, _('Derecha - MLO')],
                    [{'type': 'image', 'absolute_path': fourth_image_path, 'style': 'width:200px; height:152px'},
                     {'style': 'width: 4%; background-color: white;', 'value': ''},
                     {'type': 'image', 'absolute_path': fourth_image_path_heatmap,
                      'style': 'width:200px; height:152px'}]]
        else:
            fourth_view = [[]]

        main_header = [_('Mamografía')]
        if not self.hide_heatmaps:
            main_header += [{'style': 'width: 4%; background-color: white;', 'value': ''}, _('Áreas de interés')]

        main_base_class_str = 'mammo-no-heatmap' if self.hide_heatmaps else 'mammo'
        main = {
            'type': 'main',
            'class': main_base_class_str,
            'components':
                [
                    {
                        'type': 'table',
                        'class': 'images-with-titles',
                        'header': main_header,
                        'rows': first_view + second_view + third_view + fourth_view
                    },
                    {
                        'type': 'br'
                    }
                ]
        }
        return main

    def load_sidebar(self):

        with open(os.path.join(self.output_dir, 'text_findings.pkl'), 'rb') as f:
            report_paragraphs = pickle.load(f)

        projection_phrase = report_paragraphs['projection_phrase']
        diagnosis = report_paragraphs['diagnosis']
        calibration = report_paragraphs['calibration']

        sidebar_base_class_str = 'mammo-no-heatmap' if self.hide_heatmaps else 'mammo'
        sidebar = {
            "type": "sidebar",
            'class': sidebar_base_class_str,
            "components": [
                {
                    "type": "div",
                    "class": "relativo",
                    "items": [
                        {
                            "type": "title",
                            "text": _(
                                "Reporte de análisis automatizado por inteligencia artificial"
                            ),
                        },
                        {"type": "paragraph", "text": projection_phrase},
                        {"type": "title", "text": _('Clasificación del estudio')},
                        {"type": "paragraph", "text": diagnosis + '<br>'},
                        {"type": "title", "text": _('Score de IA')},
                        {'type': 'paragraph',
                        'text': '<i style="font-size: 11.5px;">'+_(
                                'Este Score refleja el cálculo de la IA respecto a la presencia real'
                                ' de hallazgos benignos/malignos. A mayor valor, mayor probabilidad '
                                'de presencia de un hallazgo real.' 
                                )+ '</i>',
                            'class': 'texto_reducido italics-font'
                        },
                        {"type": "paragraph", "text": calibration },
                        {
                                    "type": "div",
                                    "class": "fijo",
                                    "items": []
                        }
                    ]
                }
            ]
        }

        sidebar_fixed_items = []
        # if 'hide_mammo_specialist_note' not in self.config or not self.config['hide_mammo_specialist_note']:
        #     sidebar_fixed_items = sidebar_fixed_items + [
        #         {
        #             'type': 'title',
        #             'text': _('Aclaración para el especialista'),
        #             'class': 'titulo_reducido'
        #         },
        #         {
        #             'type': 'paragraph',
        #             'text': _(
        #                 'Con la etiqueta verde el sistema identifica aquellas mamografías que'
        #                 ' en su experiencia no requirieron biopsia dentro de los 120 días, pero'
        #                 ' que igualmente pueden tener otros hallazgos a considerar por el '
        #                 'especialista.<br>'
        #                 'La etiqueta rosa significa que los hallazgos de esta mamografía deben '
        #                 'ser revisados en mayor profundidad por el especialista según su criterio.'
        #                 ' En el entrenamiento del sistema, estos casos requirieron estudio '
        #                 'histológico dentro de los 120 días.'
        #             ),
        #             'class': 'texto_reducido italics-font'
        #         }
        #     ]

        sidebar_fixed_items += [
            {
                'type': 'title',
                'text': _('Aclaración para el paciente'),
                'class': 'titulo_reducido'
            },
            {
                'type': 'paragraph',
                'text': '<i style="font-size: 11.5px;">' +_(
                    # 'Este reporte es generado por un sistema de inteligencia artificial de soporte para'
                    # ' uso exclusivo de los profesionales médicos, no constituye en si un diagnóstico '
                    # 'médico ni una opinión profesional, ni necesariamente va a estar de acuerdo con '
                    # 'el diagnóstico, opinión, o conducta que tome su profesional tratante. Siga '
                    # 'siempre todas las recomendaciones del profesional de la salud.'
                    'Este reporte es de uso exclusivo para profesionales médicos, no constituye en sí '
                    'un diagnóstico médico ni una opinión profesional, ni necesariamente va a estar de '
                    'acuerdo con el diagnóstico, opinión o conducta que tome su profesional tratante. '
                    'Siga siempre todas las recomendaciones del profesional.'
                    ) + '</i>',
                'class': 'texto_reducido italics-font'
            },
            {
                'type': 'title',
                'text': _('Referencias'),
                'class': 'titulo_reducido'
            },

        #     { '<table class="mammo-references" >'+ \
        #     '<tr>  '+\
        #         '<td><i class="green_circle"> </i></td> '+\
        #         '<td>'+ _('Etiqueta Verde: sin hallazgos de relevancia que requieran biopsia.')+ '</td>  '+\
        #     '</tr>'+\
        #     '<tr>'+  \
        #         '<td><i class="circle_with_dashed_border"> </i></td> '+\
        #         '<td>' + _('Etiqueta Amarilla: probable hallazgo benigno.')+ '</td> '+ \
        #     '</tr>'+\
        #     '<tr>'+  \
        #         '<td><i class="circle_with_border"> </i></td> '+\
        #         '<td>'+ _(' Etiqueta Rosa: Los hallazgos de esta mamografía deben ser revisados en mayor \
        #         profundidad por el especialista según su criterio. En el entrenamiento del sistema, \
        #         estos casos requirieron estudio histológico dentro de los 120 días.')+'</td> ' + \
        #     '</tr>'+\
        #    ' </table>'
        #     }

            {
                'type':'table',
                'class':'mammo-references',
                'rows':[
                    [
                        '<i class="green_circle_references" ></i>'
                    ,
                       '<i style="font-size: 11px;">'+ _(' Etiqueta Verde: sin hallazgos de relevancia.')+'</i>'
                    ],
                    ['<i class="circle_with_dashed_border_references" ></i>',
                    '<i style="font-size: 11px;">'+_(' Etiqueta Amarilla: probable hallazgo benigno.')+'</i>'
                    ],
                    ['<i class="circle_with_border_references" ></i>',
                    '<i style="font-size: 11px;">'+ _(' Etiqueta Rosa: Los hallazgos de esta mamografía deben ser revisados \
                         por el especialista según su criterio. En el entrenamiento del sistema, \
                         estos casos requirieron estudio histológico dentro de los 120 días.')+'</i>'
                    ]
                ]
            },
            {
                'type': 'br'
            }
        ]

        sidebar['components'][0]['items'][7]['items'] = sidebar_fixed_items
        return sidebar

    def get_report_data(self):
        report_data = {
            'components': [{
                'type': 'page',
                'class': 'mammo ' + self.institution_logo_class,
                'components': [
                    self.header,
                    self.sidebar,
                    self.main,
                    self.footer(1)
                ]
            }
            ]
        }
        return report_data
