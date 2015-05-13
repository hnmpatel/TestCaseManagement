import xlrd

class Helper(object):
    def __init__(self):
        pass
        
    def parse_xls(self, file_data):
        ret = self.upload_file(file_data)
        data = []
        testcase = {}
        if ret:
            xls_workbook = xlrd.open_workbook("/tmp/test.xls")
            xls_sheet = xls_workbook.sheet_by_index(0)
            for rn in range(19,xls_sheet.nrows):
                
                expected_result = xls_sheet.cell(rn,5).value
                if expected_result == "":
                    title = xls_sheet.cell(rn,1).value
                else:
                    testcase = {}
                    testcase['expected_result'] = expected_result
                    testcase['steps'] = xls_sheet.cell(rn,1).value
                    testcase['title'] = title
                    data.append(testcase)
        return data
                
    def upload_file(self, file_data):
        file_name = file_data['file']
        try:
            with open('/tmp/test.xls', 'w+') as destination:
                for chunk in file_name.chunks():
                    destination.write(chunk)
                destination.close()
            return True
        except:
            return False
        