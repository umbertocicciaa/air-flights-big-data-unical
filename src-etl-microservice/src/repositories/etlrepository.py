import os

class EtlRepository:
    def createInputPath(self, input_path):
        return os.path.join('/tmp', input_path.filename)
    
    def createOutputPath(self, output_path):
        return os.path.join('/mnt/shared-filesystem/outputs/', output_path.filename)
    
    def saveFile(self, file, file_path):
        file.save(file_path)
    
