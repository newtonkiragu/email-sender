import csv
from typing import List,Dict
class SimpleCsvHandler:
    def __init__(self, *args, **kwargs):
        pass
    def read(self,f) -> List[Dict]:
        with open(f) as close_data:
            csvfile = csv.DictReader(close_data)
            return list(csvfile)
    def write(self,data:List[Dict],f) -> bool:
        k = data[0].keys()
        with open(f, 'w') as csvfile:
            dict_writer = csv.DictWriter(csvfile, k)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        return True