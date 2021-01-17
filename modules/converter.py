import subprocess
import requests
from os import getcwd, remove


class Converter:

    def __init__(self):
        self.WORKDIR = getcwd()

    def download(self, url):
        """
        Download source video from _url_
        :param url: source video url
        :return: status dict
        """
        try:
            req = requests.get(url)
            if 200 <= req.status_code < 400:
                source = req.content
            else:
                return {'status': 'error', 'error': 'request code ' + str(req.status_code)}
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            filename = url.split('/').pop()
            if filename.split('.').pop() != 'webm':
                return {'status': 'error', 'error': 'wrong extension'}
            file = open(self.WORKDIR+'/files/' + filename, 'wb')
            file.write(source)
            file.close()
            return {'status': 'success', 'path': self.WORKDIR+'/files/' + filename}

    def to_gif(self, filename):
        """
        Convert source file to GIF
        :param filename: source file path
        :return:
        """
        filename_gif = ''.join(filename.split('.')[:-1]) + '.gif'
        command = "/usr/bin/ffmpeg -i {} -y " \
                  "-filter_complex " \
                  "'fps=10,scale=320:-1:flags=lanczos,split [o1] [o2];[o1] " \
                  "palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse' {}".format(filename, filename_gif)
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL,
                           stderr=open('ffmpeg_error.log', 'a'))
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            return {'status': 'success', 'path': filename_gif}

    def to_mp4(self, filename):
        """
        Convert source file to MP4
        :param filename: source file path
        :return: status dict
        """
        filename_mp4 = ''.join(filename.split('.')[:-1]) + '.mp4'
        command = "/usr/bin/ffmpeg -i {} -strict -2 -y {}".format(filename, filename_mp4)
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL,
                           stderr=open('ffmpeg_error.log', 'a'))
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            return {'status': 'success', 'path': filename_mp4}

    def delete(self, path):
        """
        Delete file path
        :param path: file path
        :return: status dict
        """
        try:
            remove(path)
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            return {'status': 'success'}
