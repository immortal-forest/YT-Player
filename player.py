import pafy
import vlc
import time
import datetime
from pynput.keyboard import Key, Listener
from utils import write_to, write_history


return_value = 0
instance = vlc.Instance()
# disable the vlc logging
instance.log_unset()
player = instance.media_player_new()


def get_audio_url(video_url):
    video = pafy.new(video_url)
    best_audio = video.getbestaudio()
    return best_audio.url


def on_key_press(key):
    global return_value
    if key == Key.media_next:
        player.stop()
    if key == Key.media_previous:
        return_value = -1
        player.stop()
    elif key == Key.media_play_pause:
        if player.is_playing():
            player.pause()
            print("Player: Paused ", end='\r')
        else:
            player.play()
            print("Player: Playing", end='\r')
            


def on_key_release(key):
    global return_value
    if key == Key.f1:
        return_value = 1
        player.stop()



def play_music(url):
    global player, return_value, instance
    return_value = 0
    is_opening = False
    is_playing = True
    
    with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        try:
            audio_url = get_audio_url(url)
        except KeyboardInterrupt:
            print("Interrupted by the user!")
            return "Break"
        
        media = instance.media_new(audio_url)
        player_states = ["State.Playing", "State.NothingSpecial", "State.Opening", "State.Paused"]
        try:
            media.get_mrl()
            player.set_media(media)
            player.play()
        except Exception as e:
            write_to("res/error.txt", f"{datetime.datetime.now()} - {str(e)} -> `{url}`\n", 0, 'a', None, False)
            print("Error in MRL!\nRetrying...\033[F\033[F")
            time.sleep(5)
            return play_music("https://youtu.be/" + url.replace("https://www.youtube.com/watch?v=", ""))

        try:        
            while str(player.get_state()) in player_states:
                if str(player.get_state()) == "State.Opening" and is_opening is False:
                    print("Player: Loading", end='\r')
                    write_history("res/usr/player-history.txt", datetime.datetime.now(), f"Played --> {url}\n")
                    is_opening = True

                if str(player.get_state()) == "State.Playing" and is_playing is False:
                    print("Player: Playing", end='\r')
                    is_playing = True
            player.stop()
            return "Success", return_value
        except KeyboardInterrupt:
            player.stop()
            print("Interrupted by the user!")
            return "Break", return_value
