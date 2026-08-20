import fs from "fs";
import katex from "katex";

const htmlPath = process.argv[2];
let html = fs.readFileSync(htmlPath, "utf8");

html = html.replace(
  /<span class="math-src" data-display="([01])">([\s\S]*?)<\/span>/g,
  (_, display, tex) => {
    const decoded = tex
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">");
    return katex.renderToString(decoded, {
      displayMode: display === "1",
      throwOnError: false,
      output: "html",
      strict: "ignore",
    });
  },
);

fs.writeFileSync(htmlPath, html);
console.log("Rendered KaTeX in", htmlPath);
