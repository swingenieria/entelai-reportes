from mock import patch, mock_open, Mock
from pdfreport.report_data import mammo_report_data


@patch('pdfreport.report_data.base_report_data.ReportData._download_files')
@patch('pdfreport.report_data.mammo_report_data.MammoReportData.load_sidebar', side_effect=[''])
def test_mammo_report_data_init(mock_load_sidebar, mock_download_file, event):
    mrd = mammo_report_data.MammoReportData(event)
    assert(mrd)


@patch('pdfreport.report_data.base_report_data.ReportData._download_files')
@patch('pdfreport.report_data.mammo_report_data.path.isfile', return_value=True)
@patch('pdfreport.report_data.base_report_data.boto3')
@patch('pdfreport.report_data.mammo_report_data.pickle.load')
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_mammo_report_data_load_main_and_sidebar_without_heatmap(
    mock_open, mock_load, mock_boto, mock_isfile, mock_download_file, event
):
    session = Mock()
    session.client.return_value = 'clente'
    mock_boto.Session.return_value = session
    event['config'] = '{"hide_heatmaps": true}'

    mrd = mammo_report_data.MammoReportData(event)

    assert mrd.hide_heatmaps
    assert mrd.main['class'] == 'mammo-no-heatmap'
    # assert that all rows of the main grid have only 1 images --> 1 element
    for i in range(8):
        assert len(mrd.main['components'][0]['rows'][i]) == 1
    assert mrd.sidebar['class'] == 'mammo-no-heatmap'


@patch('pdfreport.report_data.base_report_data.ReportData._download_files')
@patch('pdfreport.report_data.mammo_report_data.path.isfile', return_value=True)
@patch('pdfreport.report_data.base_report_data.boto3')
@patch('pdfreport.report_data.mammo_report_data.pickle.load')
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_mammo_report_data_load_main_and_sidebar_with_heatmap(
    mock_open, mock_load, mock_boto, mock_isfile, mock_download_file, event
):
    session = Mock()
    session.client.return_value = 'client'
    mock_boto.Session.return_value = session
    event['config'] = '{"hide_heatmaps": false}'

    mrd = mammo_report_data.MammoReportData(event)

    assert not mrd.hide_heatmaps
    assert mrd.main['class'] == 'mammo'
    # assert that all rows of the main grid have 2 images and 1 gap --> 3 elements
    for i in range(8):
        assert len(mrd.main['components'][0]['rows'][i]) == 3
    assert mrd.sidebar['class'] == 'mammo'
