import nbformat
from nbconvert import HTMLExporter, WebPDFExporter


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
notebook_filename = "test.ipynb"
with open(notebook_filename, "r", encoding="utf-8") as f:
    notebook = nbformat.read(f, as_version=4)
from pprint import pprint as pp
import code

code.interact(local=locals())
# Extract desired outputs and markdown cells
extracted_cells = extract_outputs(notebook)

# Combine the extracted cells into a new notebook structure
final_notebook = combine_cells_to_notebook(extracted_cells)

# Convert to HTML
html_exporter = WebPDFExporter()
body, resources = html_exporter.from_notebook_node(final_notebook)
final_pdf_filename = "final_output.pdf"
with open(final_pdf_filename, "wb") as f:  # Use 'wb' for binary write
    f.write(body)
# Save the final HTML output
# final_html_filename = "final_output.html"
# save_html(body, final_html_filename)

print(f"Final document saved to {final_pdf_filename}")
