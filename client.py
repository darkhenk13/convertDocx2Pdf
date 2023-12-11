import shutil
from multiprocessing import Pool
import requests

def action(i):
    with open("template.docx", 'rb') as f:
        r = requests.post("http://192.168.50.141:6000/docx2pdf", files={
            'upload_file': f
        }, stream=True)

        if r.status_code == 200:
            with open('out/out{}.pdf'.format(i + 1), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print(r.status_code, r.content)


s = requests.Session()

if __name__ == '__main__':
    action(1)
