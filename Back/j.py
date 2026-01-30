
import os
from fpdf import FPDF
import cv2
def gen(img, txt):
    i = 0
    path = r"report_requests\Puser_report"
    file = f"report_requests\Puser_report\i{i}.pdf"
    if not os.path.exists(path):
        os.makedirs(path)
    image = cv2.imread(img)
    normalized_image = cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
    normalized_image = cv2.resize(normalized_image, (640, 640), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{path}\i_aug.jpg", normalized_image)
    image = cv2.imread(str(img[:-8]+".jpg"))
    normalized_image = cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
    normalized_image = cv2.resize(normalized_image, (640, 640), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{path}\i.jpg", normalized_image)

    while os.path.exists(file):
        i += 1
        file = f"report_requests\Puser_report\i{i}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",'', size=25)
    pdf.cell(200, 10, txt="This report is generated automatically", ln=1, align='C')
    pdf.image(path+r"\i_aug.jpg", x=None,y=None, w=190, h=140 )
    pdf.set_font("Arial", '', size=14)
    pdf.cell(200, 10, txt="Image augmeted", ln=1, align='C')

    pdf.set_font("Arial", '', size=14)
    pdf.cell(200, 10, txt=txt[:-63], ln=1, align='C')
    pdf.cell(200, 10, txt=txt[90:], ln=1, align='C')

    pdf.image(path + r"\i.jpg", x=None, y=None, w=190, h=140)
    pdf.set_font("Arial", '', size=14)
    pdf.cell(200, 10, txt="Image original", ln=1, align='C')

    pdf.output(file)
    return(file)