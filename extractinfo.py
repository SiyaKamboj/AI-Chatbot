#import text from pdf
import fitz #made to work with pdf's
def extract_text_from_pdf(pdf_file_path):
    try:
        doc=fitz.open(pdf_file_path) #open the pdf file on path
        pdf_text="" #initialize empty string to store extracted text from pdf
        for page_num in range(doc.page_count): #loop through each page
            page=doc.load_page(page_num) #load in the current page
            pdf_text += page.get_text("text") #get all the text on this page
        doc.close()
        return pdf_text
    except Exception as e:
        return f"Error extracting text: {e}"
    
#pdf_path="Landon-Hotel.pdf"
pdf_path="Triton-Television-Constitution-Draft.pdf"
extracted_text= extract_text_from_pdf(pdf_path)
file= open("pdf-text.txt", "w", encoding='utf-8')
file.write(extracted_text)

# #import text from website
# import requests
# from bs4 import BeautifulSoup

# target_url="https://www.landonhotel.com"

# response=requests.get(target_url)

# if response.status_code==200:
#     soup=BeautifulSoup(response.content, 'html.parser')

#     text=""
#     for paragraph in soup.find_all('p'):
#         text+= paragraph.get_text()

#     with open('website_text.txt', 'w') as text_file:
#         text_file.write(text)

#     print("Text extracted and saved succesfully")
