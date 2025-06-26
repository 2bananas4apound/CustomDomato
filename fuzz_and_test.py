#!/usr/bin/env python3
import argparse
import subprocess
import glob
import os
import logging
import datetime

# ── helpers ────────────────────────────────────────────────────────────
def generate_samples(generator_py, output_dir, count):
    cmd = ["python", generator_py,
           "--output_dir", output_dir,
           "--no_of_files", str(count)]
    subprocess.run(cmd, check=True)

def convert_html_to_js(extractor_script, html_dir, js_dir):
    os.makedirs(js_dir, exist_ok=True)
    subprocess.run(
        ["python", extractor_script,
         "--input_dir",  html_dir,
         "--output_dir", js_dir],
        check=True
    )

def test_js_samples(jshost, js_dir, log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    pattern = os.path.join(js_dir, "*.js")
    for js_file in sorted(glob.glob(pattern)):
        logging.info("=== Testing %s ===", js_file)
        try:
            proc = subprocess.run(
                [jshost, js_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            out = proc.stdout.decode("utf-8", errors="ignore")
            err = proc.stderr.decode("utf-8", errors="ignore")

            if proc.returncode != 0:
                logging.error("%s → return code %d", js_file, proc.returncode)
            else:
                msg = f"{js_file} ran successfully with no syntax errors"
                print(msg)
                logging.info(msg)

            if out:
                logging.info("STDOUT:\n%s", out)
            if err:
                logging.info("STDERR:\n%s", err)
        except Exception as exc:
            logging.exception("Exception while running jshost: %s", exc)

# ── main entry ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML fuzz, extract JS, and test with jshost.exe"
    )
    parser.add_argument("--generator", default="generator.py",
                        help="Path to Domato's generator.py")
    parser.add_argument("--extractor", default="extractor_js.py",
                        help="Path to extractor_js.py")
    parser.add_argument("--jshost", default="jshost.exe",
                        help="Path to jshost.exe")
    parser.add_argument("--output_dir", default="fuzzed",
                        help="Directory for generated HTML")
    parser.add_argument("--output_js_dir", default="output_js",
                        help="Directory for extracted JS")
    parser.add_argument("--count", type=int, default=100,
                        help="Number of HTML files to generate")
    parser.add_argument("--log_js", default=None,
                        help="Log file for JS crash reports")
    args = parser.parse_args()

    # make sure output dirs exist
    os.makedirs(args.output_dir,    exist_ok=True)
    os.makedirs(args.output_js_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_js = args.log_js or f"js-crashes-{timestamp}.log"

     # ── start with a clean log file ───────────────────────────
    if os.path.exists(log_js):                     # <── NEW
        os.remove(log_js)                          # <── NEW
    # ──────────────────────────────────────────────────────────

    # pipeline
    generate_samples(args.generator, args.output_dir, args.count)
    convert_html_to_js(args.extractor, args.output_dir, args.output_js_dir)
    test_js_samples(args.jshost, args.output_js_dir, log_js)

    print(f"JS testing complete. Logs written to {log_js}")

if __name__ == "__main__":
    main()
