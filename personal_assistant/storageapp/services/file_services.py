import re
from django.shortcuts import render
from django.contrib.auth.models import User
from storages.backends.dropbox import DropBoxStorage

from storageapp.models import File, FileTypes, FileExtensions



class FileServices:
    reg_ex_existance = r'\.[^./\\]+$'
    dbx_storage = DropBoxStorage()
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

    @classmethod
    def get_file_info(cls, request):
        file = request.FILES.get('file')
        owner_inst: User = User.objects.get(id=request.user.id)
        user_file_name = request.POST.get('user_input')

        try:
            extension = re.findall(cls.reg_ex_existance, file.name)[0]
            extension_inst: FileExtensions = FileExtensions.objects.get(name=extension)
        except FileExtensions.DoesNotExist:
            extension_inst: FileExtensions = FileExtensions.objects.get(id=1)

        type_inst: FileTypes = extension_inst.category

        if user_file_name:
            file_name = user_file_name
        else:
            file_name = file.name

        return owner_inst, type_inst, extension_inst, file_name

    @classmethod
    def save_file_dropbox_and_get_new_name(cls, request):
        file = request.FILES.get('file')

        dropbox_file_name = cls.dbx_storage.save(file.name, file)
        return dropbox_file_name


    @classmethod
    def delete_file(cls, file):
        cls.dbx_storage.delete(file.dropbox_file_name)
        file.delete()
        return 'File deleted'

    @classmethod
    def downlaod_file(cls, file):
        url = cls.dbx_storage.url(file.dropbox_file_name)
        return url

    @classmethod
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

    @staticmethod
    def render_files_list(request):
        fields = File.get_fields_list()

        all_files_types = [type.name for type in FileTypes.objects.all()]

        if not request.GET.getlist('filter_type'):
            files_types_enabled = all_files_types
        else:
            files_types_enabled = request.GET.getlist('filter_type')
        how_order = int(request.GET.get('category')) if request.GET.get('category') else 0
        reverse_order = '-' if '-' in files_types_enabled else ''
        files_types_obj = [FileTypes.objects.get(name=name) for name in files_types_enabled if name != '-']
        files_list = (File.objects.filter(owner=request.user.id)
                      .filter(file_type__in=files_types_obj)
                      .order_by(f'{reverse_order}{fields[how_order]}'))

        return render(request, 'storageapp/files_list.html', context={'files_list': files_list,
                                                                      'files_types_enabled': files_types_enabled,
                                                                      'file_fields': fields,
                                                                      'all_files_types': all_files_types})

