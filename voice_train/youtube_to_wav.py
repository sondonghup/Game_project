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

    def youtube_dl(self, title):
        request = self.youtube.search().list(
            q = title,
            order = 'viewCount',
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
                                         'preferredquality' : '192'}],
                    }
        
        with youtube_dl.YoutubeDL(ydl_opts)as ydl:
            ydl.download([player])

if __name__ == '__main__':
    title = input('이름 : ')

    youtube_to_wav = youtubewav()
    youtube_to_wav.youtube_dl(title)