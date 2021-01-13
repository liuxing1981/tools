import os
import zipfile
z = zipfile.ZipFile('Arithmetic_100.zip', 'w')
z.write(os.path.join(os.getcwd(),'dist','Arithmetic_100.exe'))
z.close()