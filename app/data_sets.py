import data_sets.config
import data_sets.data_set
from mara_app.monkey_patch import patch


@patch(data_sets.config.data_sets)
def _data_sets():
    return [
        data_sets.data_set.DataSet(
            id='pypi-downloads', name='PyPI downloads',
            database_alias='dwh', database_schema='pypi_dim', database_table='downloads_data_set',
            default_column_names=['Download date', 'Project', 'Project version',
                                  'Installer', 'Python version', '# Downloads'],
            use_attributes_table=True),

    ]


patch(data_sets.config.charts_color)(lambda: '#d83751')
