import fitz  # PyMuPDF
import os
import json

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages_text = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text("text").strip()
        if text:  # skip empty pages
            pages_text.append({
                "page": i + 1,
                "text": text
            })

    doc.close()
    return pages_text

def save_as_json(pages_text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pages_text, f, indent=2, ensure_ascii=False)

def save_as_txt(pages_text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for page in pages_text:
            f.write(f"\n\n--- Page {page['page']} ---\n")
            f.write(page['text'])

if __name__ == "__main__":
    # Input paths
    input_folder = "electronics_knowledge"
    output_folder = "extracted_text"

    os.makedirs(output_folder, exist_ok=True)

    files = [
        "EEE-11th Edition-Electronic Devices and Circuit Theory.pdf",
        "EEE-R P JainDigital-Electronics-text-book-1.pdf"
    ]

    for file_name in files:
        input_path = os.path.join(input_folder, file_name)
        base_name = os.path.splitext(file_name)[0].replace(" ", "_").replace("-", "_")
        json_output = os.path.join(output_folder, f"{base_name}.json")
        txt_output = os.path.join(output_folder, f"{base_name}.txt")

        print(f"🔍 Extracting from: {file_name}")
        pages = extract_text_from_pdf(input_path)

        print(f"💾 Saving to {json_output} and {txt_output}")
        save_as_json(pages, json_output)
        save_as_txt(pages, txt_output)

    print("✅ Text extraction complete.")
