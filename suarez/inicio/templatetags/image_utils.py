from django import template
from django.conf import settings
import os
from urllib.parse import unquote

register = template.Library()

@register.simple_tag
def webp_url(image_url):
    """
    Returns the URL for the WebP version of an image if it exists on disk.
    Otherwise returns the original URL.
    Usage: {% webp_url object.image.url %}
    """
    if not image_url:
        return ''
    
    # Check if it's already webp
    if image_url.lower().endswith('.webp'):
        return image_url
        
    # Unquote URL to handle special characters like 'ñ' for disk check
    unquoted_url = unquote(image_url)
    
    # Construct the absolute path on disk to check for existence
    if unquoted_url.startswith(settings.MEDIA_URL):
        relative_path = unquoted_url[len(settings.MEDIA_URL):]
        disk_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    elif unquoted_url.startswith(settings.STATIC_URL):
        relative_path = unquoted_url[len(settings.STATIC_URL):]
        static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
        disk_path = os.path.join(static_dir, relative_path)
    else:
        return image_url

    base_path, ext = os.path.splitext(disk_path)
    webp_disk_path = base_path + ".webp"

    if os.path.exists(webp_disk_path):
        base_url, ext = os.path.splitext(image_url)
        return f"{base_url}.webp"
    
    return image_url

@register.simple_tag
def version_url(image_url, size=None):
    """
    Returns the URL for a specific sized version of an image if it exists on disk.
    Else returns the original image.
    Usage: {% version_url image_url 800 %}
    """
    if not image_url:
        return ''
    
    base_url, ext = os.path.splitext(image_url)
    # Correct base name handling
    target_base = base_url[:-5] if base_url.lower().endswith('.webp') else base_url
    
    if size:
        variant_url = f"{target_base}_{size}.webp"
    else:
        variant_url = f"{target_base}.webp"

    # Check existence
    unquoted_url = unquote(variant_url)
    if unquoted_url.startswith(settings.MEDIA_URL):
        rel = unquoted_url[len(settings.MEDIA_URL):]
        disk_path = os.path.join(settings.MEDIA_ROOT, rel)
    elif unquoted_url.startswith(settings.STATIC_URL):
        rel = unquoted_url[len(settings.STATIC_URL):]
        static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
        disk_path = os.path.join(static_dir, rel)
    else:
        return image_url

    if os.path.exists(disk_path):
        return variant_url
    
    return image_url

@register.simple_tag
def get_srcset(image_url):
    """
    Generates a srcset string containing only existing WebP variants.
    """
    if not image_url:
        return ''
    
    base_url, _ = os.path.splitext(image_url)
    target_base = base_url[:-5] if base_url.lower().endswith('.webp') else base_url
    
    variants = []
    for s in [400, 800, 1200]:
        v_url = f"{target_base}_{s}.webp"
        unquoted = unquote(v_url)
        
        if unquoted.startswith(settings.MEDIA_URL):
            rel = unquoted[len(settings.MEDIA_URL):]
            disk_path = os.path.join(settings.MEDIA_ROOT, rel)
        elif unquoted.startswith(settings.STATIC_URL):
            rel = unquoted[len(settings.STATIC_URL):]
            static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
            disk_path = os.path.join(static_dir, rel)
        else:
            continue
            
        if os.path.exists(disk_path):
            variants.append(f"{v_url} {s}w")
            
    return ", ".join(variants)
