from storageapp.models import FileTypes, FileExtensions

file_types = ['other', 'images', 'videos', 'archives', 'docs', 'sound', 'applications']
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
message = ['.eml', '.mht', '.mhtml', '.nws'],
docs = ['.css', '.csv', '.html', '.htm', '.txt', '.bat', '.c', '.h', '.ksh', '.pl', '.rtx', '.tsv', '.py', '.etx',
        '.sgm', '.sgml', '.vcf', ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".rtf", ".xml",
        ".ini"],
videos = ['.mp4', '.mpeg', '.m1v', '.mpa', '.mpe', '.mpg', '.mov', '.qt', '.webm', '.avi', '.movie', '.wav', ".mkv"]
archives = [".zip", ".tar", ".tgz", ".gz", ".7zip", ".7z", ".iso", ".rar"]

def create_tables(cls):
    for type in cls.file_types:
        inst = FileTypes.objects.create(name=type)
        if type == 'images':
            for ext in cls.images:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type == 'videos':
            for ext in cls.videos:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type == 'archives':
            for ext in cls.archives:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type == 'docs':
            for ext in cls.docs:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type == 'sound':
            for ext in cls.sound:
                FileExtensions.objects.create(name=ext, category=inst)
        elif type == 'applications':
            for ext in cls.applications:
                FileExtensions.objects.create(name=ext, category=inst)