

def is_supported_format(file):
    if file.lower().endswith(('.fb2', '.fb2.zip', '.zip', '.epub')):
        return True
    else:
        return False
