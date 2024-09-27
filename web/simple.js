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
