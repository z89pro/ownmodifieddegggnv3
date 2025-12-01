import instaloader
import os
import logging

logger = logging.getLogger(__name__)

def download_instagram_post(url, target_dir):
    """
    Download Instagram post using Instaloader.
    Returns the path to the downloaded file (video or image).
    """
    L = instaloader.Instaloader(
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )

    # Extract shortcode from URL
    shortcode = url.split("/")[-2]
    
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=target_dir)
        
        # Find the downloaded file
        for file in os.listdir(target_dir):
            if file.endswith(".mp4"):
                return os.path.join(target_dir, file)
            elif file.endswith(".jpg"):
                return os.path.join(target_dir, file)
                
        return None
    except Exception as e:
        logger.error(f"Instaloader error: {e}")
        return None
