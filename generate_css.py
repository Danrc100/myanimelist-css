import urllib.request
import json
import time
import re

USERNAME = "Danrc_100"

def fetch_list(username, list_type="anime"):
    items = []
    offset = 0
    while True:
        url = f"https://myanimelist.net/{list_type}list/{username}/load.json?offset={offset}&status=7"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if not data:
                    break
                items.extend(data)
                if len(data) < 300:
                    break
                offset += 300
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching {list_type} list at offset {offset}: {e}")
            break
    return items

def get_hd_url(thumbnail_url):
    if not thumbnail_url:
        return ""
    # Remove resolution tag e.g. /r/192x272 or /r/96x136
    hd_url = re.sub(r'/r/\d+x\d+', '', thumbnail_url)
    # Remove query parameters like ?s=...
    hd_url = hd_url.split('?')[0]
    return hd_url

def generate_css():
    css_lines = []
    
    # Process Anime
    print(f"Fetching anime list for {USERNAME}...")
    anime_list = fetch_list(USERNAME, "anime")
    print(f"Found {len(anime_list)} anime.")
    for item in anime_list:
        anime_id = item.get("anime_id")
        img_url = item.get("anime_image_path")
        if anime_id and img_url:
            hd_url = get_hd_url(img_url)
            css_lines.append(f'.data.image a[href^="/anime/{anime_id}/"]:before{{background-image:url({hd_url});}}')
            
    # Process Manga
    print(f"Fetching manga list for {USERNAME}...")
    manga_list = fetch_list(USERNAME, "manga")
    print(f"Found {len(manga_list)} manga.")
    for item in manga_list:
        manga_id = item.get("manga_id")
        img_url = item.get("manga_image_path")
        if manga_id and img_url:
            hd_url = get_hd_url(img_url)
            css_lines.append(f'.data.image a[href^="/manga/{manga_id}/"]:before{{background-image:url({hd_url});}}')
            
    # Write to capas.css
    with open("capas.css", "w", encoding="utf-8") as f:
        f.write("\n".join(css_lines))
    print(f"Successfully generated capas.css with {len(css_lines)} rules.")

if __name__ == "__main__":
    generate_css()
