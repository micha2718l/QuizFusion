import nbconvert
from nbconvert import HTMLExporter, WebPDFExporter
import nbformat
from pathlib import Path

# Path to your notebook
dir_in = Path("notebooks")
dir_out = Path("out")
name = "kinematics"
outputs = ["pdf", "html"]
# outputs = ["html"]


def extract_outputs(notebook, include_markdown=True):
    extracted_cells = []
    for cell in notebook.cells:
        print("getting cell")
        if cell.cell_type == "code" and cell.outputs:
            for output in cell.outputs:
                print("getting out")
                print(output.output_type)
                if (
                    output.output_type == "execute_result"
                    or output.output_type == "display_data"
                ):
                    # Create a markdown cell with the formatted output
                    print(output["data"])
                    markdown_cell = nbformat.v4.new_markdown_cell(
                        output["data"]["text/markdown"] or output["data"]["text/latex"]
                    )
                    print("?")
                    extracted_cells.append(markdown_cell)
        elif include_markdown and cell.cell_type == "markdown":
            extracted_cells.append(cell)
    return extracted_cells


def combine_cells_to_notebook(cells):
    combined_notebook = nbformat.v4.new_notebook()
    combined_notebook.cells = cells
    return combined_notebook


def save_html(html_body, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_body)


# Load the notebook
with open(dir_in / f"{name}.ipynb", "r", encoding="utf-8") as f:
    notebook = nbformat.read(f, as_version=4)

notebook.cells = extract_outputs(notebook)

if "pdf" in outputs:
    pdf_exporter = WebPDFExporter()
    body_pdf, _ = pdf_exporter.from_notebook_node(notebook)

    with open(dir_out / f"{name}.pdf", "wb") as f:
        f.write(body_pdf)

if "html" in outputs:
    html_exporter = HTMLExporter()
    body_html, _ = html_exporter.from_notebook_node(notebook)

    with open(dir_out / f"{name}.html", "w", encoding="utf-8") as f:
        f.write(body_html)

print(f"Notebook converted to {outputs}")
