#!/usr/bin/env python3
import argparse
import subprocess
import glob
import os
import logging
import datetime

def generate_samples(generator_py, output_dir, count):
    cmd = ["python", generator_py, "--output_dir", output_dir,
           "--no_of_files", str(count)]
    subprocess.run(cmd, check=True)

def convert_html_to_js(extractor_script, html_dir, js_dir):
    os.makedirs(js_dir, exist_ok=True)
    subprocess.run(
        ["python", extractor_script,
         "--input_dir", html_dir,
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
        logging.info(f"=== Testing {js_file} ===")
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
                logging.error(f"{js_file} → Return code {proc.returncode}")
            else:
                # Print and log a success message when returncode == 0
                success_msg = f"{js_file} ran successfully with no syntax errors"
                print(success_msg)
                logging.info(success_msg)

            if out:
                logging.info(f"STDOUT:\n{out}")
            if err:
                logging.info(f"STDERR:\n{err}")
        except Exception as exc:
            logging.exception(f"Exception while running jshost: {exc}")

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

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.output_js_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_js = args.log_js or f"js-crashes-{timestamp}.log"

    generate_samples(args.generator, args.output_dir, args.count)
    convert_html_to_js(args.extractor, args.output_dir, args.output_js_dir)
    test_js_samples(args.jshost, args.output_js_dir, log_js)

    print(f"JS testing complete. Logs written to {log_js}")

if __name__ == "__main__":
    main()
