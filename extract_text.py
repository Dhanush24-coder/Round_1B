import fitz  # PyMuPDF
import os

def extract_text_from_pdfs(pdf_folder):
    extracted_data = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            doc = fitz.open(filepath)

            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if "lines" in block:
                        text = ""
                        font_sizes = []
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text += span["text"] + " "
                                font_sizes.append(span["size"])

                        text = text.strip()
                        if text:
                            extracted_data.append({
                                "document": filename,
                                "page": page_num + 1,
                                "text": text,
                                "avg_font_size": sum(font_sizes) / len(font_sizes) if font_sizes else 0
                            })

            doc.close()
    
    return extracted_data


if __name__ == "__main__":
    data = extract_text_from_pdfs("pdfs")
    for item in data:
        print(item)
