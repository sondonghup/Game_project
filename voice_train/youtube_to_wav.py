import os
import googleapiclient.discovery
import yt_dlp as youtube_dl
import ffmpeg

class youtubewav():
    def __init__(self):
        api_service_name = 'youtube'
        api_version = 'v3'
        DEVELOPER_KEY = os.environ['youtube_api_key']
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY
        )

    '''
     def download(self, url_list):
        """Download a given list of URLs."""
        url_list = variadic(url_list)  # Passing a single URL is a common mistake
        outtmpl = self.params['outtmpl']['default']
        if (len(url_list) > 1
                and outtmpl != '-'
                and '%' not in outtmpl
                and self.params.get('max_downloads') != 1):
            raise SameFileError(outtmpl)

        for url in url_list:
            self.__download_wrapper(self.extract_info)(
                url, force_generic_extractor=self.params.get('force_generic_extractor', False))

        return self._download_retcode

    def download_with_info_file(self, info_filename):
        with contextlib.closing(fileinput.FileInput(
                [info_filename], mode='r',
                openhook=fileinput.hook_encoded('utf-8'))) as f:
            # FileInput doesn't have a read method, we can't call json.load
            infos = [self.sanitize_info(info, self.params.get('clean_infojson', True))
                     for info in variadic(json.loads('\n'.join(f)))]
        for info in infos:
            try:
                self.__download_wrapper(self.process_ie_result)(info, download=True)
            except (DownloadError, EntryNotInPlaylist, ReExtractInfo) as e:
                if not isinstance(e, EntryNotInPlaylist):
                    self.to_stderr('\r')
                webpage_url = info.get('webpage_url')
                if webpage_url is None:
                    raise
                self.report_warning(f'The info failed to download: {e}; trying with URL {webpage_url}')
                self.download([webpage_url])
        return self._download_retcode

    '''

    def youtube_dl(self, title):
        request = self.youtube.search().list(
            q = title,
            order = 'rating',
            part = 'snippet',
            maxResults = 1
        )
        response = request.execute()
        print(response)
        chan_id = response['items'][0]['id']['videoId']
        player = f'https://www.youtube.com/watch?v={chan_id}'
        print('url : ' + player)
        ydl_opts = {'format' : 'bestaudio',
                    'postprocessors' : [{'key' : 'FFmpegExtractAudio',
                                         'preferredcodec' : 'wav',
                                        #  'preferredquality' : '192'
                                         }],
                    }
        
        with youtube_dl.YoutubeDL(ydl_opts)as ydl:
            ydl.download(player)

if __name__ == '__main__':
    title = input('이름 : ')

    youtube_to_wav = youtubewav()
    youtube_to_wav.youtube_dl(title)