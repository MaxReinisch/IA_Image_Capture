START = 0
END = 2
TIMEOUT = 30
HEIGHT=1080
WIDTH = 1920
import requests
import sys
# import os

def getArchiveURL(url):
    return "https://web.archive.org/web/2/" + url

def getImgURL(archived_url, height, width):
    parts = archived_url.split("/")
    timestamp = parts[4]
    target = "/".join(parts[5:]).replace("\n", "")
    newurl = f"http://crawl-services.us.archive.org:8200/wayback?url="+target+"&timestamp="+timestamp+"&height="+str(height)+"&width="+ str(width)+"&nav=1"
    return newurl

def saveImg(imgURL, name):
    r = requests.get(imgURL, timeout=TIMEOUT, stream=True)
    try:
        with open(f"imgs/{name}.jpg", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
    except:
        print(f"Failed to write to file: imgs/{name}.jpg ")
        return
def main():
    filename = sys.argv[1]
    try:
        with open(filename, "r") as f:
            urls = f.readlines()
    except:
        print("File not found.  Please try again.")
        exit(-1)
    # if(~ os.path.isdir("/imgs")):
    #     print("Making new directory: /imgs")
    #     os.mkdir("/imgs")

    for i, url in enumerate(urls[START:min(END, len(urls))]):
        if(url.startswith("http://web.archive.org/web/")):
            imgURL = getImgURL(url, HEIGHT, WIDTH)
            try:
                saveImg(imgURL, f"img_{i}")
            except:
                continue
            print(f"{(i+1)/min(END, len(urls))*100}% complete")
        elif(url.startswith("http")):
            archive_url = getArchiveURL(url)
            imgURL = getImgURL(archive_url, HEIGHT, WIDTH)
            try:
                saveImg(imgURL, f"img_{i}")
            except:
                continue
            print(f"{(i+1)/min(END, len(urls))*100}% complete")
main()
