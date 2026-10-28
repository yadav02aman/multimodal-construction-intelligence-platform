"""
Sample data and synthetic reference images for 1-click testing.
Generates realistic visual test images for PPE and Concrete Crack diagnostics.
"""
import io
from PIL import Image, ImageDraw, ImageFont

def generate_sample_ppe_image() -> bytes:
    """Generate a realistic test image depicting a construction site with workers."""
    width, height = 800, 500
    img = Image.new("RGB", (width, height), color="#2A3439")
    draw = ImageDraw.Draw(img)

    # Sky and background buildings
    draw.rectangle([0, 0, width, 220], fill="#3A4D59")
    draw.rectangle([60, 60, 200, 260], fill="#273746")
    draw.rectangle([240, 40, 360, 280], fill="#1C2833")
    draw.rectangle([400, 80, 520, 270], fill="#2C3E50")

    # Tower crane outline
    draw.line([(680, 280), (680, 40)], fill="#F39C12", width=6)
    draw.line([(550, 60), (760, 60)], fill="#F39C12", width=5)
    draw.line([(680, 40), (620, 60)], fill="#F39C12", width=3)
    draw.line([(680, 40), (740, 60)], fill="#F39C12", width=3)
    draw.line([(620, 60), (620, 160)], fill="#BDC3C7", width=2) # Hook cable

    # Scaffolding & structural concrete slab
    draw.rectangle([0, 260, width, 500], fill="#7F8C8D")
    draw.rectangle([0, 330, width, 500], fill="#566573")

    # Scaffolding grid
    for x in range(30, width - 100, 90):
        draw.line([(x, 200), (x, 380)], fill="#95A5A6", width=3)
        draw.line([(x, 260), (x + 90, 260)], fill="#95A5A6", width=2)
        draw.line([(x, 320), (x + 90, 320)], fill="#95A5A6", width=2)
        draw.line([(x, 200), (x + 90, 260)], fill="#7F8C8D", width=1)

    # Worker 1: Fully Compliant (Yellow helmet, orange vest, harness)
    # Head & Helmet
    draw.ellipse([180, 270, 205, 295], fill="#F4D03F") # Helmet
    draw.ellipse([183, 278, 202, 295], fill="#E59866") # Face
    # High-vis Vest
    draw.rectangle([175, 296, 210, 345], fill="#E67E22")
    draw.line([(185, 296), (185, 345)], fill="#ECF0F1", width=3) # Reflective strip
    draw.line([(200, 296), (200, 345)], fill="#ECF0F1", width=3)
    # Legs & Steel boots
    draw.rectangle([178, 345, 192, 390], fill="#2C3E50")
    draw.rectangle([193, 345, 207, 390], fill="#2C3E50")
    draw.rectangle([176, 385, 194, 398], fill="#17202A") # Boot
    draw.rectangle([191, 385, 209, 398], fill="#17202A") # Boot

    # Worker 2: High Risk Non-Compliant (NO Helmet, Dark clothes, near slab edge)
    # Head with dark hair (NO helmet)
    draw.ellipse([460, 255, 485, 280], fill="#212F3D")
    draw.ellipse([463, 263, 482, 280], fill="#D35400") # Face
    # Dark Shirt (NO High-vis vest)
    draw.rectangle([455, 281, 490, 335], fill="#34495E")
    # Pants & Slippers / open shoes
    draw.rectangle([458, 335, 472, 380], fill="#5D6D7E")
    draw.rectangle([473, 335, 487, 380], fill="#5D6D7E")
    draw.rectangle([457, 375, 473, 386], fill="#E74C3C") # Open sandals!

    # Site Signage / Warning
    draw.rectangle([620, 320, 760, 420], fill="#F1C40F", outline="#B7950B", width=3)
    draw.rectangle([625, 325, 755, 360], fill="#C0392B")
    draw.text((635, 333), "CAUTION / DANGER", fill="#FFFFFF")
    draw.text((630, 370), "HARD HAT & HARNESS", fill="#17202A")
    draw.text((630, 388), "AREA - OSHA COMPLIANT", fill="#17202A")

    # Informative Overlay label
    draw.rectangle([20, 20, 320, 55], fill="#1A252F")
    draw.text((30, 26), "SITE SAFETY AUDIT REFERENCE", fill="#00D2D3")
    draw.text((30, 40), "ISO 45001 / OSHA 1926.95 INSPECTION", fill="#BDC3C7")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def generate_sample_crack_image() -> bytes:
    """Generate a realistic test image depicting a concrete shear crack with measurement scale."""
    width, height = 800, 500
    img = Image.new("RGB", (width, height), color="#BDC3C7")
    draw = ImageDraw.Draw(img)

    # Concrete texture simulation (grey tones with aggregate speckles)
    for y in range(0, height, 8):
        shade = 175 + (y % 15)
        draw.rectangle([0, y, width, y + 8], fill=(shade, shade + 3, shade + 1))

    # Beam boundary / Chamfer line
    draw.line([(0, 60), (width, 60)], fill="#7F8C8D", width=4)
    draw.line([(0, 440), (width, 440)], fill="#566573", width=5)

    # Diagonal structural shear crack (zig-zag realistic fracture)
    crack_coords = [
        (120, 80), (160, 115), (180, 140), (220, 185), (250, 210),
        (290, 245), (340, 280), (410, 310), (460, 345), (520, 375),
        (590, 405), (650, 435)
    ]
    # Draw crack core and spalling shadows
    for i in range(len(crack_coords) - 1):
        p1 = crack_coords[i]
        p2 = crack_coords[i + 1]
        draw.line([p1, p2], fill="#17202A", width=5)
        # Secondary micro-fissure
        if i in [3, 4, 7]:
            draw.line([(p1[0], p1[1]), (p1[0] + 35, p1[1] + 15)], fill="#424949", width=2)

    # Spalling / aggregate exposure area near middle
    draw.polygon([(320, 260), (370, 255), (385, 290), (330, 295)], fill="#7B7D7D", outline="#2C3E50")
    # Rust stain from corroding rebar
    draw.ellipse([345, 270, 375, 295], fill="#B9770E")

    # Engineering measurement scale card placed near crack
    draw.rectangle([480, 220, 640, 290], fill="#FFFFFF", outline="#2C3E50", width=2)
    draw.rectangle([480, 220, 640, 240], fill="#E74C3C")
    draw.text((490, 224), "CRACK MONITOR RULER", fill="#FFFFFF")
    # Ticks
    for x in range(490, 630, 10):
        h = 10 if (x - 490) % 20 == 0 else 5
        draw.line([(x, 260), (x, 260 + h)], fill="#000000", width=1)
    draw.text((490, 274), "0mm    10mm    20mm", fill="#333333")

    # Measurement indicator arrow
    draw.line([(310, 245), (460, 255)], fill="#C0392B", width=2)
    draw.rectangle([250, 170, 410, 205], fill="#1C2833")
    draw.text((258, 176), "EST. WIDTH: 2.8 mm", fill="#E74C3C")
    draw.text((258, 190), "DIAGONAL SHEAR (IS 456)", fill="#F4D03F")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()
