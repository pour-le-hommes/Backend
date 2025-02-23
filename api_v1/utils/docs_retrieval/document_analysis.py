from pypdf import PdfReader
import sys
sys.setrecursionlimit(10000)

from pypdf import PdfReader

def text_processing(old_txt:str):
    new_txt = old_txt.replace(
        "\nThis content downloaded from 139.195.36.26 on Fri, 22 Sep 2017 12:11:42 UTC\nAll use subject to http://about.jstor.org/terms",
        ""
    ) 
    new_txt = new_txt.replace(
        "-\n ",
        ""
    )
    return new_txt

def open_pdf():
    pdf_path = r'data/WHITE_BOOK_OF_THE_1978_STUDENTS_STRUGGLE.pdf'
    
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        return f"Error opening PDF: {e}"

    num_pages = len(reader.pages)
    print(f"Number of pages: {num_pages}")
    full_text = {}  # Initialize an empty string to hold the entire document

    for i in range(num_pages):
        if i==0:
            continue
        try:
            page = reader.pages[i]
            text = page.extract_text()
            processed_text = text_processing(text)
            full_text[f"page_{i}"]= f"\n{processed_text}"  # Append each page's text with page markers
        except Exception as e:
            return f"Error extracting text from page {i+1}: {e}"

    return full_text

# Call the function
open_pdf()

