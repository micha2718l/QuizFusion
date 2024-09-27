console.log("Hello, world!");
function showProblem() {
  statementInput = document.getElementById("statementInput").value;
  eel
    .show_problem(statementInput)()
    .then((response) => {
      document.getElementById("markdownInput").value = response;
      renderMarkdown();
    });
}

function renderMarkdown() {
  const input = document.getElementById("markdownInput").value;
  document.getElementById("outputArea").innerHTML = input;
  resetMathJax();
}

function clearEditor() {
  document.getElementById("markdownInput").value = "";
  document.getElementById("outputArea").innerHTML = "";
}

function exportContent() {
  const content = document.getElementById("markdownInput").value;
  const blob = new Blob([content], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "content.md";
  link.click();
}

function previewLatex() {
  // Placeholder for LaTeX preview functionality
  alert("LaTeX Preview coming soon...");
}

function preview() {
  const v = document.getElementById("Value_0_value").value;
  const u = document.getElementById("Value_0_unit").value;
  const s = document.getElementById("Value_0_sigfigs").value;
  const p = document.getElementById("Value_0_pre_zeros").value;
  eel
    .preview(v, u, s, p)()
    .then((response) => {
      document.getElementById("output").innerHTML = response;
      resetMathJax();
    });
}
all_inputs = document.querySelectorAll(".input");
all_inputs.forEach((element) => {
  element.oninput = preview;
});
//document.getElementById("markdownInput").oninput = function () {
//  renderMarkdown();
//};
