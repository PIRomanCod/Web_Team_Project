from storageapp.models import File, FileTypes, FileExtensions
from personal_assistant import settings
from django.contrib.auth.models import User
from django.core.files.storage import get_storage_class
import re
import dropbox
class FileServices:
    reg_ex = r'\.[^./\\]+$'
    dbx_class = get_storage_class(settings.DROPBOX_STORAGE)
    dbx_storage = dbx_class()

    @classmethod
    def get_info_from_file(cls, request):

        file = request.FILES.get('file')
        owner_inst: User = User.objects.get(id=request.user.id)

        try:
            extension = re.findall(cls.reg_ex, file.name)[0]
            extension_inst: FileExtensions = FileExtensions.objects.get(name=extension)
        except FileExtensions.DoesNotExist:
            extension_inst: FileExtensions = FileExtensions.objects.get(id=1)

        type_inst: FileTypes = extension_inst.category

        file_name = file.name

        return owner_inst, type_inst, extension_inst, file_name

    @classmethod
    def save_file_dropbox_and_get_url(cls, request):
        file = request.FILES.get('file')
        dropbox_file_name = cls.dbx_storage.save(file.name, file)

        url = cls.dbx_storage.url(file.name)
        return url, dropbox_file_name

    @staticmethod
    def get_user_files_list(user_id):
        result = File.objects.filter(owner=user_id)
        return result

    @classmethod
    def delete_file(cls, file):
        cls.dbx_storage.delete(file.dropbox_file_name)
        file.delete()
        return True
