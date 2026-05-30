"""
Google Colab runner for Operation Cypher Nexus.

Upload Datasets (2).zip to the Colab session, then run:
    !python colab_runner.py
"""

from pathlib import Path

from cypher_nexus_project import find_dataset_zip, run_all_parts


def main():
    dataset_zip = find_dataset_zip()

    if dataset_zip is None:
        try:
            from google.colab import files

            print("Please upload Datasets (2).zip.")
            uploaded = files.upload()
            zip_names = [name for name in uploaded if name.lower().endswith(".zip")]
            dataset_zip = Path(zip_names[0]) if zip_names else None
        except ImportError:
            dataset_zip = None

    if dataset_zip is None:
        print("Dataset ZIP was not found. The program will use clearly marked fallback demo data.")
    else:
        print(f"Using dataset ZIP: {dataset_zip}")

    results = run_all_parts(dataset_zip_path=dataset_zip, output_dir="outputs")
    print(results["summary"]["output_text"])
    print("Open the outputs folder to view detailed Part 1-8 results.")


if __name__ == "__main__":
    main()
