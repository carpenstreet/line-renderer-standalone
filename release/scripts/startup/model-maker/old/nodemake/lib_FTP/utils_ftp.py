def ftp_open(filename, Download_Path, ftp):

    with open(Download_Path + filename, "wb") as fd:
        ftp.retrbinary("RETR " + filename, fd.write)
        ftp.set_pasv(False)
