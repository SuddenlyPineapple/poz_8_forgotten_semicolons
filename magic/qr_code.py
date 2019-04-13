import qrcode.image.svg

def gen_qrcode(code):
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(str(code), image_factory=factory)
    img.save(str(code)+'.svg')

def decode_qrcode(image):
    pass