import re
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydata"]

class ServerSideTable(object):
    
    def __init__(self, request, data, column_list,collection):
        self.result_data = None
        self.cardinality_filtered = 0
        self.cardinality = 0
        self.request_values = request.values
        self.columns = sorted(column_list, key=lambda col: col['order'])
        print(self.columns)
        self.mycol = mydb[collection]
        self.dataq = data
        self._run()
    def _run(self):

        countCol = self.mycol.find(self.dataq).count()
        self.cardinality = int(countCol)

        sSearch = self.request_values.get('sSearch', "")    
        if sSearch:
            regx = re.compile(sSearch, re.IGNORECASE)
            agg = []
            for dbcolmn in self.columns:
                agg.append({ dbcolmn['column_name']:{'$regex':regx} })
            self.dataq['$or'] = agg
        countColFilt = self.mycol.find(self.dataq).count()
        self.cardinality_filtered = int(countColFilt)

        sorted_data = self._custom_sort()

        skip = int(self.request_values['iDisplayStart'])
        length = int(self.request_values['iDisplayLength'])
        if skip <= 1:
            skip = 0

        DATA_SAMPLE = []
        for data in self.mycol.find(self.dataq,{'_id':0}).sort(sorted_data['column_name'],sorted_data['sort']).skip(skip).limit(length):
            DATA_SAMPLE.append(data)        
        self.result_data = DATA_SAMPLE
        
    def _extract_rows_from_data(self, data):
        
        rows = []
        for x in data:
            row = {}
            for column in self.columns:
                default = column['default']
                data_name = column['data_name']
                column_name = column['column_name']
                row[column_name] = x.get(data_name, default)
            rows.append(row)
        return rows        
        

    def _custom_sort(self):
        
        def is_reverse(str_direction):
            return -1 if str_direction == 'desc' else 1

        if (self.request_values['iSortCol_0'] != "") and (int(self.request_values['iSortingCols']) > 0):
            for i in range(0, int(self.request_values['iSortingCols'])):
                column_number = int(self.request_values['iSortCol_' + str(i)])
                column_name = self.columns[column_number]['column_name']
                sort_direction = self.request_values['sSortDir_' + str(i)]
                sort_direction_reverse = int(is_reverse(sort_direction))

            
        return {'column_name':column_name,'sort':sort_direction_reverse}


    def output_result(self):
        
        output = {}
        output['sEcho'] = str(int(self.request_values['sEcho']))
        output['iTotalRecords'] = str(self.cardinality)
        output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        output['data'] = self.result_data

        print(output)

        return output