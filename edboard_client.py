from __future__ import unicode_literals
import requests
import glob
import lzma
import gzip
import os
import unicodedata

baseUrl = 'http://ed-board.net'

path = u'log/*.xz'
pathSave = 'log/import.log'
pathSaveTmp = 'log/import.tmp.gz'

files=glob.glob(path)
for file in files:
  filename = os.path.basename(file)
  filenametmp = unicodedata.normalize('NFD', filename).encode('ascii', 'ignore')
  pathSaveTmp = 'log/'+filenametmp.decode('ascii')+'.tmp.gz'

  with open(pathSave, 'a+') as inF:
    find = 0

    for line in open(pathSave):
      if filename in line:
        find = 1

    if find == 0:
      inF.write(filename+'\n');
      with lzma.open('log/'+filename) as f:
        file_content = f.read()
        with gzip.open(pathSaveTmp, 'wb') as tmp:
          tmp.write(file_content);
          f.close()
      r = requests.post(baseUrl+'/stats.php', files={'edce': open(pathSaveTmp, 'rb')})
      os.remove(pathSaveTmp)




  inF.close()

print("Done !")