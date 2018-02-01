from django.core.files.storage import FileSystemStorage

def saveOnProfile(request,filename):
    file = request.FILES[filename]
    fs = FileSystemStorage()
    fn = fs.save(file.name,file)
    url = fs.url(fn)
    return url