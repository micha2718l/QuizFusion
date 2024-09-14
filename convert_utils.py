import time
import os
from pathlib import Path

from nbconvert import HTMLExporter, WebPDFExporter
import nbformat

dir_in = Path("notebooks")
dir_out = Path("out")
template_file = "exam/index.html.j2"
template_paths = [os.path.join(os.path.dirname(__file__), "Templates")]


def extract_outputs(notebook, include_markdown=True):
    extracted_cells = []
    for cell in notebook.cells:
        if cell.cell_type == "code" and cell.outputs:
            for output in cell.outputs:
                if (
                    output.output_type == "execute_result"
                    or output.output_type == "display_data"
                ):
                    # Create a markdown cell with the formatted output
                    markdown_cell = nbformat.v4.new_markdown_cell(
                        output["data"].get("text/markdown", False)
                        or output["data"].get("text/latex", False)
                        or "![image](data:image/png;base64,"
                        + output["data"].get("image/png", "")
                        + ")"
                    )
                    extracted_cells.append(markdown_cell)
        elif include_markdown and cell.cell_type == "markdown":
            extracted_cells.append(cell)
    return extracted_cells


def open_notebook(fn):
    # Load the notebook
    with open(fn, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)
    notebook.cells = extract_outputs(notebook)
    return notebook


def export_pdf(notebook, resources, name):
    print(f"Exporting PDF {name}")
    pdf_exporter = WebPDFExporter(template_file=template_file)
    pdf_exporter.template_paths += template_paths
    body_pdf, _ = pdf_exporter.from_notebook_node(notebook, resources)
    fn = dir_out / f"{name}.pdf"
    with open(fn, "wb") as f:
        f.write(body_pdf)
    return fn


def export_html(notebook, resources, name):
    html_exporter = HTMLExporter(template_file=template_file)
    html_exporter.template_paths += template_paths
    body_html, _ = html_exporter.from_notebook_node(notebook, resources)
    fn = dir_out / f"{name}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(body_html)
    return fn


def export(notebook, name, resources={}, pdf=True, html=False):
    print(f"Exporting {name} to pdf: {pdf} and html: {html}")
    if pdf:
        export_pdf(notebook, resources, name)
    if html:
        export_html(notebook, resources, name)


def detect_file_changes(path, pdf=True, html=False, interval=1):
    last_modified = os.path.getmtime(path)
    while True:
        current_modified = os.path.getmtime(path)
        if current_modified != last_modified:
            print(f"Detecting changes in {path}")
            notebook = open_notebook(path)
            export(notebook, path.stem, {}, pdf, html)
            print(f"Done exporting.")
            last_modified = current_modified
        time.sleep(interval)
