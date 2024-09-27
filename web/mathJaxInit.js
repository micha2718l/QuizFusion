init_mathjax = function () {
  if (window.MathJax) {
    // MathJax loaded
    MathJax.Hub.Config({
      TeX: {
        equationNumbers: {
          autoNumber: "AMS",
          useLabelIds: true,
        },
      },
      tex2jax: {
        inlineMath: [
          ["$", "$"],
          ["\\(", "\\)"],
        ],
        displayMath: [
          ["$$", "$$"],
          ["\\[", "\\]"],
        ],
        processEscapes: true,
        processEnvironments: true,
      },
      displayAlign: "center",
      CommonHTML: {
        linebreaks: {
          automatic: true,
        },
      },
    });

    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
  }
};

resetMathJax = function () {
  if (window.MathJax) {
    MathJax.Hub.Typeset()();
  } else {
    console.warn("MathJax not loaded");
  }
};

window.onload = function () {
  init_mathjax();
};
