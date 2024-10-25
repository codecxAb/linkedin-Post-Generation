import pdfplumber

# Path to your PDF file
pdf_path = 'cv.pdf'
txt_path = 'extracted_resume.txt'

with pdfplumber.open(pdf_path) as pdf:
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                txt_file.write(text)

print(f'Text extracted and saved to {txt_path}')