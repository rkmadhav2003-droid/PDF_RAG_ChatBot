import pymupdf

pdf = pymupdf.open(r"D:\Projects\RAG_Project\doc\MADHAV R KRISHNAN_Resume.pdf")

page = pdf[0]

data = page.get_text("dict")
print(data.keys())

for block in data["blocks"]:
    if "lines" not in block:
        continue
    
    for line in block["lines"]:
        line_text = ""
        for span in line["spans"]:
            line_text += span["text"]
            print(
            span["text"],
            span["font"],
            span["size"],
            span["flags"]
            )
        print(line_text)