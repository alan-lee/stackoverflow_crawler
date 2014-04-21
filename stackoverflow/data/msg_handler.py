import json
from datetime import date
import os


def process_msg(addr, msg):
    json_msg = json.loads(msg)
    method = json_msg['method']

    if method == 'get':
        query_date = json_msg['date']
        if query_date is None:
            query_date = date.today()
        page = json_msg['page']
        if page is None:
            page = 1
        page_size = json_msg['page_size']
        if page_size is None:
            page_size = 20

        end = page * page_size
        start = end - page_size

        json_file = "json/%s.json" % (query_date,)
        if not os.path.exist(json_file):
            return '[]'

        file_obj = open("json/%s.json" % (query_date,), 'rb')

        output = list()

        line_number = 1
        line = file_obj.readline()
        while line:
            if line_number in range(start, end + 1):
                output.append(line)

            if line_number > end:
                break

            line_number += 1

            line = file_obj.readline()

        return json.dumps(output)

if __name__ == '__main__':
    msg = dict()
    msg['date'] = '2014-4-20'
    msg['page'] = 2
    msg['page_size'] = 20
    msg['method'] = 'get'
    result = process_msg('1.1.1.1', json.dumps(msg))

    print result