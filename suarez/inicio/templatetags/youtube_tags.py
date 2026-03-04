import re
from django import template

register = template.Library()

@register.filter(name='youtube_embed')
def youtube_embed(url):
    """
    Converts any YouTube URL to a high-compatibility embed URL.
    - Handles watch?v=, youtu.be/, shorts/, live/
    - Cleans up extra parameters
    - Returns standard youtube.com/embed/ for maximum browser support
    """
    if not url:
        return ""
    
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
    video_id = get_youtube_id(url)
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}?autoplay=0&rel=0"
    return url
