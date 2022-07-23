import pafy
import vlc
import time
import datetime
from utils import write_to, write_history


def get_audio_url(video_url):
    video = pafy.new(video_url)
    best_audio = video.getbestaudio()
    return best_audio.url


def play_music(url):
    is_opening = False
    is_playing = True
    try:
        audio_url = get_audio_url(url)
    except KeyboardInterrupt:
        print("Interrupted by the user!")
        return "Break"
    
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(audio_url)
    try:
        media.get_mrl()
        player.set_media(media)
        player.play()
    except Exception as e:
        write_to("res/error.txt", f"{datetime.datetime.now()} - {str(e)} -> `{url}`\n", 0, 'a', None, False)
        print("Error in MRL!\nRetrying...\r")
        time.sleep(2)
        return play_music("https://youtu.be/" + url.replace("https://www.youtube.com/watch?v=", ""))

    player_states = ["State.Playing", "State.NothingSpecial", "State.Opening"]
    try:
        while str(player.get_state()) in player_states:
            if str(player.get_state()) == "State.Opening" and is_opening is False:
                print("Player: Loading", end='\r')
                write_history("res/usr/player-history.txt", datetime.datetime.now(), f"Played --> {url}\n")
                is_opening = True

            if str(player.get_state()) == "State.Playing" and is_playing is False:
                print("Player: Playing", end='\r')
                is_playing = True
        print("Player: Finish ", end='\r')
        player.stop()
        return "Success"
    except KeyboardInterrupt:
        player.stop()
        print("Interrupted by the user!")
        return "Break"
