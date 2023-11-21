import pytest


@pytest.fixture
def event():
    return {
        'bucket_name': 'bucket_name',
        'study_prefix': '1.0.0.0.0.0',
        'PatientName': 'fulano',
        'PatientID': '000000',
        'PatientSex': 'F',
        'age': '30Y',
        'title': 'titulo',
        'StudyDescription': 'descripcion',
        'StudyDate': '20200101',
        'language': 'es_AR',
        'config': '{}',
        'send_error_pdf': 'False',
        'institution_logo': 'url',
        'institution_logo_class': 'logo_class',
        'version_tag': 'alpha',
        'prev_study_name': '',
        'prev_study_date': ''
    }


@pytest.fixture(scope='session', autouse=True)
def install_l10n():
    import gettext as g
    trans = g.translation('spam', 'locale', fallback=True)
    trans.install('gettext')
    _ = trans.gettext
