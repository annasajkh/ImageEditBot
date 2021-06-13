"""Generates impact font memes"""
from PIL import Image, ImageFont, ImageDraw

def get_font(image):
    """Create font with dynamic size"""
    font_size = int(image.width / 8)
    return ImageFont.truetype("impact.ttf", size=font_size)

def draw_caption_text(x, y, border_size, caption, font, draw):
    """Draws the caption at the x and y, you need to initiate the draw first"""
    border_color = (0,0,0)
    text_color = (255, 255, 255)

    # Draw the border
    draw.text((x-border_size, y), caption, fill=border_color, font=font)
    draw.text((x+border_size, y), caption, fill=border_color, font=font)
    draw.text((x, y-border_size), caption, fill=border_color, font=font)
    draw.text((x, y+border_size), caption, fill=border_color, font=font)

    # Draw the caption
    draw.text((x, y), caption, text_color, font)

def generate_text_position(image, caption, font, draw, bottom=False):
    """Returns the position the text should be given the image, caption and font"""

    # Get caption size
    caption_width, caption_height = draw.textsize(caption, font)

    # Upper text position
    caption_position = (image.height-caption_height)/10

    if bottom:
        # The bottom caption position
        caption_position = (image.height-caption_height)-caption_position
    
    # Position horizontally
    x_position = (image.width-caption_width)/2
    
    return (x_position, caption_position)
    

def make_caption(image, caption, bottom_caption=None):
    """Generates impact font caption, if bottom_caption isn't specified there will be no bottom text"""
    font = get_font(image)

    # Create draw object on the image
    draw = ImageDraw.Draw(image)

    # TODO: Dynamic border size
    border_size = 2

    # Get the caption position
    x, upper_text_position = generate_text_position(image, caption, font, draw)

    # Draw the upper caption
    draw_caption_text(x, upper_text_position, border_size, caption, font, draw)

    # Draw the bottom caption
    if bottom_caption: 
        # Get the caption position
        x, bottom_text_position = generate_text_position(image, bottom_caption, font, draw, True)

        # Draw the text
        draw_caption_text(x, bottom_text_position, border_size, bottom_caption, font, draw)

    return image
