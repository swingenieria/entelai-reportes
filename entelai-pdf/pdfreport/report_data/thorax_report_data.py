import csv
import logging
from os import path
from .base_report_data import ReportData

logger = logging.getLogger()


class ThoraxReportData(ReportData):
    def __init__(self, event, output_dir=None):
        super().__init__(event, output_dir)
        self.header["entelai_img"]["absolute_path"] = path.join(
            "..", "images", "logo_entelai-thorax.png"
        )
        table_file = (
            event["table_file"] if "table_file" in event else "thorax_results.csv"
        )
        table_file_path = path.join(output_dir, table_file)
        with open(table_file_path) as fin:
            csvin = csv.reader(fin)
            header = next(csvin, [])
            self.table = dict(zip(header, zip(*csvin)))

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
        first_image_path = path.join(self.output_dir, "pred_img0_report.png")
        if path.isfile(first_image_path):
            first_view = [
                [_("Proyección ") + self.table["description-0"][0].upper()],
                [
                    {
                        "type": "image",
                        "absolute_path": first_image_path,
                        "style": "width:100%;",
                    }
                ],
            ]
        else:
            first_view = [[]]

        second_image_path = path.join(self.output_dir, "pred_img1_report.png")

        desc_1 = self.table["description-1"][0]
        if not path.isfile(second_image_path):
            second_image_path = path.join(self.output_dir, "no_bg_ori_img.png")
            desc_1 = self.table["description-0"][0] + " Original"

        if path.isfile(second_image_path):
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
        else:
            second_view = [[]]

        if "hide_heatmap" in self.table and self.table["hide_heatmap"][0] == "yes":

            main = {
                "type": "main",
                "components": [
                    {
                        "type": "table",
                        "class": "images-with-titles",
                        "header": [_("Radiografía de Tórax")],
                        "rows": first_view,
                    },
                    {"type": "br"},
                ],
            }
        else:
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
        text = self.findings["text"]
        diagnosis = self.findings["diagnosis"]
        findings = self.findings["findings"]

        sidebar = {
            "type": "sidebar",
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
                        {"type": "paragraph", "text": text},
                        {"type": "title", "text": _("Hallazgos radiológicos")},
                        {"type": "paragraph", "text": diagnosis},
                        {"type": "list", "class": "item_hallazgo", "items": findings},
                        {
                            "type": "div",
                            "class": "fijo",
                            "items": [
                                {
                                    "type": "title",
                                    "class": "titulo_reducido",
                                    "text": _("Aclaración para el médico"),
                                },
                                {
                                    "type": "paragraph",
                                    "text": _(
                                        "El porcentaje presente en cada hallazgo refleja el grado de certeza que posee "
                                        "el algoritmo para su predicción. Cuanto más alto el porcentaje, "
                                        "mayor es el grado de certeza ante un determinado hallazgo. "
                                        "Por el contrario, porcentajes más bajos, reflejan un menor grado de certeza. "
                                        "Esto puede deberse a factores del entrenamiento del algoritmo o "
                                        "propios de la imagen (hallazgo pequeño, atípico o imagen de baja calidad). "
                                        "Los mapas de calor son una representación visual de los sectores de la radiografía "
                                        "que fueron más relevantes para el algoritmo de inteligencia artificial en su predicción. "
                                        "Sin embargo, estas áreas pueden no necesariamente coincidir con "
                                        "los sectores radiológicamente relevantes para el diagnóstico del hallazgo."
                                    ),
                                    "class": "texto_reducido",
                                },
                                {
                                    "type": "title",
                                    "class": "titulo_reducido",
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
                    ],
                },
            ],
        }
        return sidebar

    def get_report_data(self):
        report_data = {
            "components": [
                {
                    "type": "page",
                    "class": "torax " + self.institution_logo_class,
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


class CovidThoraxReportData(ThoraxReportData):
    def __init__(self, event, output_dir=None):
        ReportData.__init__(self, event, output_dir)
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
        img_types = ["AP", "PA"]
        for img_type in img_types:
            image_path = path.join(self.output_dir, img_type, f"{img_type}.png")
            if path.isfile(image_path):
                break

        first_view = [
            [_("Proyección ") + img_type],
            [{"type": "image", "absolute_path": image_path, "style": "width:100%;"}],
        ]
        main = {
            "type": "main",
            "components": [
                {
                    "type": "table",
                    "class": "images-with-titles",
                    "header": [_("Imagen analizada")],
                    "rows": first_view,
                },
                {"type": "br"},
            ],
        }
        return main
