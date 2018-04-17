import csv
import glob
import os
import sys
import subprocess
import shutil
import xml.etree.ElementTree as ET


def main():
    if len(sys.argv) < 3 or not os.path.exists(sys.argv[1]):
        print("Error: Missing argument(s).")
        print("Example: python " + os.path.basename(sys.argv[0]) + " /absolute/path/to/project GeneralDebug")
        sys.exit(1)
    PROJECT_ROOT = sys.argv[1]
    PRODUCT_FLAVOR = sys.argv[2]

    RESULT_DIR = PROJECT_ROOT + "/build/reports/jacoco"
    
    gradlew = PROJECT_ROOT + "/gradlew"
    process = subprocess.Popen([gradlew, "jacocoTestReport" + PRODUCT_FLAVOR])
    process.wait()
    if process.returncode != 0:
        print("Error: jacocoTestReport" + PRODUCT_FLAVOR + " failed")
        sys.exit(1)

    if os.path.exists(RESULT_DIR):
        shutil.rmtree(RESULT_DIR)
    os.makedirs(RESULT_DIR)
    
    coverages = {}
    for report_csv in glob.glob(PROJECT_ROOT + "/*/build/reports/jacoco/*/jacoco.csv"):
        report_dir = os.path.dirname(report_csv)
        module = None
        
        with open(report_csv) as csvfile:
            header = next(csv.reader(csvfile))
            data = dict((h, 0) for h in header[3:])
            csvfile.seek(0)
            
            reader = csv.DictReader(csvfile)

            for row in reader:
                if module is None:
                    module = row["GROUP"]
                for key in data:
                    data[key] += int(row[key])
        if module is not None:
            coverages[module] = data
            shutil.copytree(report_dir, RESULT_DIR + "/" + module)

    header_list = ["MODULE", "INSTRUCTION", "BRANCH", "LINE", "COMPLEXITY", "METHOD"]

    html = ET.Element("html")
    head = ET.SubElement(html, "head")
    ET.SubElement(head, "title").text = "Test Coverage"
    body = ET.SubElement(html, "body")
    ET.SubElement(body, "h2").text = "Test Coverage"
    table = ET.SubElement(body, "table", attrib={"border": "1", "cellpadding": "10", "style": "border-collapse:collapse;"})
    tr_header = ET.SubElement(table, "tr")

    for header in header_list:
        ET.SubElement(tr_header, "th").text = header + (" MISSED (COVERAGE)" if header != "MODULE" else "")
    
    total_cov = dict((data_type, [0, 0]) for data_type in header_list[1:])
    for module in sorted(coverages):
        data = coverages[module]
        tr = ET.SubElement(table, "tr")
        ET.SubElement(ET.SubElement(tr, "td"), "a", attrib={"href": "./" + module + "/index.html"}).text = module
        for data_type in header_list[1:]:
            missed = data[data_type + "_MISSED"]
            covered = data[data_type + "_COVERED"]
            total = missed + covered
            total_cov[data_type][0] += missed
            total_cov[data_type][1] += covered
            if total > 0:
                ET.SubElement(tr, "td").text = "{0} of {1} ({2:.2f}%)".format(missed, total, float(covered) / total * 100.0)
            else:
                ET.SubElement(tr, "td").text = "{0} of {1} (-)".format(missed, total)

    tr_total = ET.SubElement(table, "tr")
    ET.SubElement(ET.SubElement(tr_total, "td"), "b").text = "TOTAL"
    for data_type in header_list[1:]:
        missed = total_cov[data_type][0]
        covered = total_cov[data_type][1]
        total = missed + covered
        if total > 0:
            ET.SubElement(ET.SubElement(tr_total, "td"), "b").text = "{0} of {1} ({2:.2f}%)".format(missed, total, float(covered) / total * 100.0)
        else:
            ET.SubElement(ET.SubElement(tr_total, "td"), "b").text = "{0} of {1} (-)".format(missed, total)
        pass

    ET.ElementTree(html).write(RESULT_DIR + '/report.html', encoding='utf8', method='html')
    return

if __name__ == "__main__":
    main()