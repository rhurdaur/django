""" 
Mixins
"""
class XMLExport:
    def export(self):
        print("export xml", self.data)


class DataManager():
    
    def __init__(self, exporter):
        self.exporter = exporter
    
    def manage_data(self):
        print("manage Data ...")
        
    def get_data(self):
        return [3, 3, 4]
    
    def export(self):
        self.exporter.export()
        
        
class DataManager2(XMLExport):
    
    def __init__(self):
        self.data = [3, 3, 4]
    
    def manage_data(self):
        print("manage Data ...")
        
    def get_data(self):
        return [3, 3, 4]

        
        
d = DataManager2()
d.export()