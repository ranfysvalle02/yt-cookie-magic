import browser_cookie3
import os
import yt_dlp

def export_cookies_to_file(output_file):
    """
    Fetch cookies from an incognito/private browsing session and save them to a file in Netscape cookie format.
    """
    cookies = browser_cookie3.chrome()  # Fetch cookies from Chrome (update to firefox() for Firefox)
    
    # Write cookies to a file in Netscape cookie format
    with open(output_file, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This file was generated by a script.\n")
        for cookie in cookies:
            # Use leading '#' for domains starting with '.' per Netscape format
            domain = f"#{cookie.domain}" if cookie.domain.startswith('.') else cookie.domain
            f.write(f"{domain}\t"
                    f"{'TRUE' if cookie.domain.startswith('.') else 'FALSE'}\t"
                    f"{cookie.path}\t"
                    f"{'TRUE' if cookie.secure else 'FALSE'}\t"
                    f"{cookie.expires or 0}\t"
                    f"{cookie.name}\t"
                    f"{cookie.value}\n")
    print(f"Cookies exported to {output_file}")

def download_video_with_cookies(video_url, cookies_file):
    """
    Use yt-dlp to download a video using the specified cookies file.
    """
    ydl_opts = {
        'cookiefile': cookies_file,
        'quiet': False,  # Set to True to suppress output
        'outtmpl': '%(title)s.%(ext)s',  # Output filename template
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def main():
    cookies_file = 'incognito_youtube_cookies.txt'  # File to save cookies
    video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Replace with your desired video URL
    
    # Export cookies to file (ensure this is done in an incognito/private session)
    export_cookies_to_file(cookies_file)
    
    # Use yt-dlp to download the video with the exported cookies
    try:
        download_video_with_cookies(video_url, cookies_file)
    finally:
        # Clean up: remove cookies file for security
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
            print("Cookies file removed for security.")

if __name__ == "__main__":
    main()