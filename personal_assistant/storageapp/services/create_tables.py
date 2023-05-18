"""
This module is used to create tables in the database.
"""
from storageapp.models import FileExtensions, FileTypes


def create_tables():
    """
    The create_tables function creates the tables in the database.
    It is called by manage.py when you run python manage.py create_storageapp_tables

    :return: Nothing
    :doc-author: Trelent
    """
    file_types = {'other': 'icons/other.jpeg', 'images': 'icons/image.png', 'videos': 'icons/video.png',
                  'archives': 'icons/archive.png', 'docs': 'icons/docs.png', 'sound': 'icons/audio.png',
                  'applications': 'icons/applications.jpg', 'message': 'icons/message.png'}
    applications = ['.js', '.mjs', '.json', '.webmanifest', '.dot', '.wiz', '.bin', '.a', '.o',
                    '.obj', '.so', '.oda', '.p7c', '.ps', '.ai', '.eps', '.m3u', '.m3u8', '.xlb', '.pot', '.ppa',
                    '.pps',
                    '.pwz', '.wasm', '.bcpio', '.cpio', '.csh', '.dvi', '.gtar',
                    '.hdf', '.h5', '.latex', '.mif', '.cdf', '.nc', '.p12', '.pfx', '.ram', '.pyc', '.pyo', '.sh',
                    '.shar', '.swf', '.sv4cpio', '.sv4crc', '.tcl', '.tex', '.texi', '.texinfo', '.roff', '.t',
                    '.tr', '.man', '.me', '.ms', '.ustar', '.src', '.xsl', '.rdf', '.wsdl', '.xpdl', '.exe',
                    '.msi', '.dll']
    sound = ['.3gp', '.3gpp', '.3g2', '.3gpp2', '.aac', '.adts', '.loas', '.ass', '.au', '.snd', '.mp3', '.mp2',
             '.opus', '.aif', '.aifc', '.aiff', '.ra', ".ogg", ".amr"]
    images = ['.bmp', '.gif', '.ief', '.jpg', '.jpe', '.jpeg', '.heic', '.heif', '.png', '.svg', '.tiff', '.tif',
              '.ico', '.ras', '.pnm', '.pbm', '.pgm', '.ppm', '.rgb', '.xbm', '.xpm', '.xwd']
    message = ['.eml', '.mht', '.mhtml', '.nws']
    docs = ['.css', '.csv', '.html', '.htm', '.txt', '.bat', '.c', '.h', '.ksh', '.pl', '.rtx', '.tsv', '.py', '.etx',
            '.sgm', '.sgml', '.vcf', ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".rtf", ".xml",
            ".ini"]
    videos = ['.mp4', '.mpeg', '.m1v', '.mpa', '.mpe', '.mpg', '.mov', '.qt', '.webm', '.avi', '.movie', '.wav', ".mkv"]
    archives = [".zip", ".tar", ".tgz", ".gz", ".7zip", ".7z", ".iso", ".rar"]
    other = ['unknown']


    for type_name, img in file_types.items():
        inst = FileTypes.objects.create(name=type_name, img=img)
        if type_name == 'images':
            for ext in images:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'videos':
            for ext in videos:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'archives':
            for ext in archives:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'message':
            for ext in message:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'docs':
            for ext in docs:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'sound':
            for ext in sound:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'applications':
            for ext in applications:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type_name == 'other':
            for ext in other:
                FileExtensions.objects.create(name=ext, category=inst)
