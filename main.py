import tempfile
from aiohttp import web
import os
import subprocess


async def docx2pdf_handle(request):
    with tempfile.NamedTemporaryFile() as output:
        reader = await request.multipart()
        docx = await reader.next()

        while True:
            chunk = await docx.read_chunk()
            if not chunk:
                break
            output.write(chunk)


        print(os.path.abspath(os.path.dirname(output.name)))
        p = subprocess.Popen([
            '/usr/bin/soffice',
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            os.path.abspath(os.path.dirname(output.name)),
            os.path.abspath(output.name)
        ])
        p.wait()

        path = "{}.pdf".format(output.name)
        response = web.StreamResponse(
            status=200,
            reason="OK",
        )
        response.content_type = 'application/pdf'
        await response.prepare(request)

        try:
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read()
                    if not chunk:
                        break
                    await response.write(chunk)
                    #await response
        except Exception as ex:
            print(ex)
            response = web.Response(status=400)

        print(response.content_type)
        return response

if __name__ == '__main__':
    app = web.Application()
    app.router.add_post('/docx2pdf', docx2pdf_handle)

    web.run_app(app, port=int(os.getenv('PORT', "6000")))
