import table_schemas
from serverside_table import ServerSideTable

class TableBuilder(object):
    def collect_data_serverside(self, request):
        DATA_SAMPLE = {}
        collection = "emp"
        columns = table_schemas.EMP_COLUMNS
        return ServerSideTable(request,DATA_SAMPLE, columns,collection).output_result()