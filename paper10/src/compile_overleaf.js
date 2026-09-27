#!/usr/bin/env node
/**
 * paper10/src/compile_overleaf.js
 * ===============================
 * Automated standalone compiler for the Paper 10 Overleaf package.
 * Uses the WebAssembly Tectonic engine (glyphtex-engine) with pybtex
 * to compile manuscript.tex -> manuscript.pdf in 3 clean passes.
 *
 * Usage:
 *   node paper10/src/compile_overleaf.js [overleaf_dir]
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

async function compileOverleafPackage(targetDir) {
  const overleafDir = path.resolve(targetDir || path.join(__dirname, "../overleaf"));
  console.log("Compiling Overleaf project at:", overleafDir);

  const gtePath = path.resolve("/tmp/gte/node_modules/glyphtex-engine");
  const { TexEngine } = await import(path.join(gtePath, "dist", "engine.js"));

  const wasmBuffer = fs.readFileSync(path.join(gtePath, "wasm", "tectonic_wasm.wasm"));
  const engine = await TexEngine.load(wasmBuffer);

  // Load standard TeX bundle files
  const bundleDir = "/tmp/tex_bundle";
  if (fs.existsSync(bundleDir)) {
    for (const f of fs.readdirSync(bundleDir)) {
      engine.addFile(f, fs.readFileSync(path.join(bundleDir, f)));
    }
  }

  // Load local files from overleafDir
  for (const f of fs.readdirSync(overleafDir)) {
    const fullPath = path.join(overleafDir, f);
    if (fs.statSync(fullPath).isFile() && !f.endsWith(".pdf")) {
      engine.addFile(f, fs.readFileSync(fullPath));
    }
  }

  // Load figures
  const figDir = path.join(overleafDir, "figures");
  if (fs.existsSync(figDir)) {
    for (const f of fs.readdirSync(figDir)) {
      const content = fs.readFileSync(path.join(figDir, f));
      engine.addFile(`figures/${f}`, content);
      engine.addFile(f, content);
    }
  }

  console.log("=== PASS 1: Generating auxiliary file (.aux) ===");
  const r1 = engine.compile({ entry: "manuscript.tex" });
  if (r1.status === "failed") throw new Error("Pass 1 compilation failed");

  const aux = engine.output("manuscript.aux");
  if (!aux) throw new Error("No .aux file produced");

  // Run pybtex in a temporary directory
  const tmpDir = fs.mkdtempSync("/tmp/overleaf-bib-");
  fs.writeFileSync(path.join(tmpDir, "manuscript.aux"), Buffer.from(aux));
  fs.copyFileSync(path.join(overleafDir, "references.bib"), path.join(tmpDir, "references.bib"));
  fs.copyFileSync(path.join(overleafDir, "elsarticle-num.bst"), path.join(tmpDir, "elsarticle-num.bst"));

  console.log("=== PASS 2: Processing bibliography with pybtex ===");
  execSync("pybtex manuscript.aux", { cwd: tmpDir, stdio: "inherit" });

  const bbl = fs.readFileSync(path.join(tmpDir, "manuscript.bbl"), "utf8");
  engine.addFile("manuscript.bbl", bbl);

  console.log("=== PASS 3: Compiling with bibliography ===");
  const r2 = engine.compile({ entry: "manuscript.tex" });
  if (r2.status === "failed") throw new Error("Pass 2 compilation failed");

  const aux2 = engine.output("manuscript.aux");
  if (aux2) engine.addFile("manuscript.aux", aux2);

  console.log("=== PASS 4: Final pass to resolve all cross-references ===");
  const r3 = engine.compile({ entry: "manuscript.tex" });
  if (r3.status === "failed") throw new Error("Pass 3 compilation failed");

  const pdfBytes = engine.pdf("manuscript");
  if (!pdfBytes) throw new Error("No PDF produced");

  const outPdf = path.join(overleafDir, "manuscript.pdf");
  fs.writeFileSync(outPdf, Buffer.from(pdfBytes));
  console.log("SUCCESS: Created", outPdf, `(${fs.statSync(outPdf).size} bytes)`);
}

const target = process.argv[2] || path.join(__dirname, "../overleaf");
compileOverleafPackage(target).catch(err => {
  console.error("Compilation error:", err);
  process.exit(1);
});
