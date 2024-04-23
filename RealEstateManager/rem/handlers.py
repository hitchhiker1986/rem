def handle_uploaded_file(f, apt_id):
    path=str(apt_id) + '/' + f.filename
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)