import re
from django import template

register = template.Library()

@register.filter(name='video_platform')
def video_platform(url):
    """Detects if the video is from vimeo or youtube."""
    if not url:
        return "youtube"
    if "vimeo.com" in url.lower():
        return "vimeo"
    return "youtube"

@register.filter(name='vimeo_embed_url')
def vimeo_embed_url(url):
    """Extracts Vimeo video ID and privacy hash (if present) to build the embed URL."""
    if not url:
        return None
        
    video_id = None
    privacy_hash = None
    
    # 1. Try to find the 8-11 digit ID
    id_match = re.search(r"(\d{8,11})", url)
    if id_match:
        video_id = id_match.group(1)
        
    # 2. Try to find an alphanumeric privacy hash (typically 8-10 chars at the end of the URL)
    # e.g., vimeo.com/123456789/abcdef1234
    hash_match = re.search(r"\d{8,11}/([a-zA-Z0-9]+)", url)
    if hash_match:
        privacy_hash = hash_match.group(1)
    # Alternatively, it might be passed as a query param ?h=xxx
    elif "?h=" in url or "&h=" in url:
        hash_param_match = re.search(r"[?&]h=([a-zA-Z0-9]+)", url)
        if hash_param_match:
            privacy_hash = hash_param_match.group(1)
            
    if not video_id:
        return None
        
    embed_url = f"https://player.vimeo.com/video/{video_id}"
    if privacy_hash:
        embed_url += f"?h={privacy_hash}"
        
    return embed_url

def get_youtube_id(url):
    if not url:
        return None
    video_id = None
    
    # Standard patterns
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
    elif "v=" in url:
        # Use regex for more reliability with complex URLs
        match = re.search(r"[?&]v=([^&]+)", url)
        if match:
            video_id = match.group(1)
            
    # If not found, look for common path components
    if not video_id:
        for tag in ["/shorts/", "/live/", "/embed/", "/v/"]:
            if tag in url:
                video_id = url.split(tag)[1].split("?")[0].split("&")[0]
                break
                
    # Final fallback: generic ID detection (11 chars, no slashes/dots)
    if not video_id:
        # Clean the string from potential wrapper characters
        cleaned = url.strip().split('/')[-1].split('?')[0].split('&')[0]
        if len(cleaned) == 11:
            video_id = cleaned
            
    return video_id.strip()[:11] if video_id else None

@register.filter(name='youtube_id')
def youtube_id(url):
    return get_youtube_id(url)

@register.filter(name='youtube_embed')
def youtube_embed(url):
    """
    Converts any YouTube URL to a high-compatibility embed URL.
    - Handles watch?v=, youtu.be/, shorts/, live/
    - Cleans up extra parameters
    - Returns standard youtube.com/embed/ for maximum browser support
    """
    video_id = get_youtube_id(url)
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}?autoplay=0&rel=0"
    return url
