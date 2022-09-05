from utils import COLORS as c, get_video_details, add_playlist, remove_playlist_name


EXIT = False
HELP = f"""
{c.OKCYAN}YT Player{c.ENDC}

{c.HEADER}Commands:{c.ENDC}
    {c.OKGREEN}Set a custom playlist{c.ENDC}
    {c.OKBLUE}- /set cpl <playlist title> <video url or video name or playlist url>{c.ENDC}
    {c.OKGREEN}List the playlists or a items of a playlist{c.ENDC}
    {c.OKBLUE}- /lpl <playlist title> (optional){c.ENDC}
    {c.OKGREEN}Play a custom playlist{c.ENDC}
    {c.OKBLUE}- /cpl <playlist title>{c.ENDC}
    {c.OKGREEN}Remove a custom playlist{c.ENDC}
    {c.OKBLUE}- /rpl <playlist title>{c.ENDC}
    {c.OKGREEN}Play a playlist from url{c.ENDC}
    {c.OKBLUE}- /pl <playlist url>{c.ENDC}
    {c.OKGREEN}Play a video{c.ENDC}
    {c.OKBLUE}- /v <video url>{c.ENDC}
    {c.WARNING}Close the program{c.ENDC}
    {c.FAIL}- /q{c.ENDC}

{c.BOLD}Just pass the video name or url or a playlist url if you feel lazy!{c.ENDC} 😄
"""


def show_list_results(search_results, s: str):
    question = [
        {
            'type': 'list',
            'name': 'list',
            'message': f'{s}:',
            'choices': search_results
        }
    ]
    try:
        ans = prompt(question)
    except KeyboardInterrupt:
        return {'search': 'none'}
    return ans


def prompt_user():
    question = [
        {
            'type': 'confirm',
            'message': 'Do you want to continue?',
            'name': 'continue',
            'default': False
        }
    ]
    ans = prompt(question)
    return ans['continue']


def main():
    while True:

        main_question = [
            {
                'type': 'input',
                'name': 'mq',
                'message': 'Search a song or play a YT url/playlist:'
            }
        ]
        try:
            r = str(prompt(main_question)['mq'])
        except KeyboardInterrupt:
            return prompt_user()
        if r.startswith("/rpl"):
            title = r.replace("/rpl ", "")
            n = remove_playlist_name(title)
            if n is None:
                print(f"{c.WARNING}No playlist found with name:{c.ENDC} {c.FAIL}{title.capitalize()}{c.ENDC}\n")
                continue
            else:
                print(f"{c.FAIL}Removed {c.OKBLUE}{n.get('name').capitalize()}{c.ENDC} from the {c.BOLD}playlist!{c.ENDC}")
                continue
        
        # set playlist
        if r.startswith("/set"):
            if "cpl" in r:
                r_lst = r.replace("/set ", '').replace("cpl ", '').split(" ")
                title = r_lst.pop(0)
                tmp_link = " ".join(r_lst)
                if not "://" in tmp_link:
                    lists = search_video(tmp_link)
                    link = show_list_results(lists, 'Search results')['list']
                    if link == 'none':
                        continue
                else:
                    if "playlist" in tmp_link or "list" in "tmp_link":
                        videos = load_playlist(tmp_link[tmp_link.find("list=") + 5:], False)
                        if videos is None:
                            print(f"{c.WARNING}Invalid video url!{c.ENDC}")
                            continue
                        for item in videos:
                            add_playlist(title, item[0], item[1], item[2])
                            print(f"Added {c.OKBLUE}{item[1]}{c.ENDC} to playlist -> {c.HEADER}{title.capitalize()}{c.ENDC}")
                            continue
                    link = r_lst[0]
                name, link, channel = get_video_details(link)
                if name is None:
                    print(f"{c.WARNING}Invalid video url!{c.ENDC}")
                    continue
                add_playlist(title, link, name, channel)
                print(f"Added {c.OKBLUE}{name}{c.ENDC} to playlist -> {c.HEADER}{title.capitalize()}{c.ENDC}")
                continue
        
        
        # list playlists or items from a particular playlist
        if r.startswith("/lpl"):
            title = r.replace("/lpl", "").strip()
            if title == "":
                names = list_playlists()
            else:
                names = list_playlists(title)
            if names is None:
                print(f"{c.WARNING}No playlists found!{c.ENDC}")
                continue
            if isinstance(names, str):
                num = len(names.split('\n'))
                print(f"{c.HEADER}{title.capitalize()} items ({num}):{c.ENDC}\n{c.OKBLUE}{names}{c.ENDC}\n")
                continue
            nms = ", ".join(names)
            print(f"{c.HEADER}Local Playlists:{c.ENDC} {c.OKBLUE}{nms}{c.ENDC}\n")
            continue
            
        
        # play a playlist
        if r.startswith('/cpl'):
            lists = load_playlist_from_name(r.replace("/cpl ", ''))
            if lists is None:
                print(f"{c.WARNING}No playlist found!{c.ENDC}")
                continue
            try:
                value = show_list_results(lists, 'Playlist items')['list']
            except KeyboardInterrupt:
                continue
            if value == 'none':
                continue
            stat = play_playlist(value)
            if stat:
                continue
            else:
                return True

        
        # play video url
        if r.startswith("/v"):
            play_music(r.replace("/v ", ''))
            continue
        # search playlist url
        if r.startswith("/pl"):
            playlist_itms = load_playlist(r.replace("/pl ", '')[r.find("list=") + 1:])

            if playlist_itms is None:
                print(f"{c.WARNING}No playlist found!{c.ENDC}")
                continue
            try:
                value = show_list_results(playlist_itms, 'Playlist items')['list']
            except KeyboardInterrupt:
                continue
            if value == 'none':
                continue
            stat = play_playlist(value)
            if stat:
                continue
            else:
                return True
        
        
        # play a playlist url or a video url
        if "://" in r:
            if "list" in r or "playlist" in r:
                playlist_itms = load_playlist(r[r.find("list=") + 5:])
                if playlist_itms is None:
                    print(f"{c.WARNING}No results!{c.ENDC}")
                    continue
                try:
                    index = show_list_results(playlist_itms, 'Playlist items:')['list']
                except KeyboardInterrupt:
                    continue
                if index == 'none':
                    continue
                stat = play_playlist(index)
                if stat:
                    continue
                else:
                    return True
            s = play_music(r)
            if s[0] != 'Break':
                continue
        # quit
        if r == "/q":
            return False
        if r == '':
            continue
        
        
        # if none of the above are true then search for video
        search_results = search_video(r)
        if search_results is None:
            print(f"{c.WARNING}No search results!{c.ENDC}")
            continue
        option = show_list_results(search_results, "Search Results")
        if option['list'] == 'none':
            continue
        s = play_music(option['list'])
        if s[0] == 'Break':
            continue


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) != 0:
        if args[0] == "--help":
            print(HELP)
            sys.exit()
    from PyInquirer import prompt
    from pyfiglet import Figlet

    from player import play_music
    from playlist import load_playlist, play_playlist, load_playlist_from_name, list_playlists
    from search import search_video
    
    # remove the errors printed 
    print("\033[F" + " " * 100)
    print("\033[F" + Figlet(font='slant').renderText("YT Player"))

    while True:
        if EXIT:
            break

        EXIT = not main()
    print(f"{c.OKCYAN}Closing YT player!{c.ENDC}")
    sys.exit()
