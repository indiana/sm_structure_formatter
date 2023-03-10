"""
This is a tool to  format SampleManager's structure.txt file.
"""
import sys
import re

def main():
    """
    Main function of the program
    """
    print(sys.argv)
    if sys.argv[1].lower() in ["-h", "--help", "/?"]:
        display_usage()
        sys.exit()
    if len(sys.argv) < 1 or len(sys.argv) > 3:
        print("Incorrect number of parameters.")
        display_usage()
        sys.exit()

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 1 else sys.argv[1]

    file = open(in_file, mode="r", encoding="utf8")
    in_lines = file.readlines()
    file.close()

    out_lines = []
    field_def = False
    field_str = ""
    for in_line in in_lines:
        line = in_line.strip().lower()
        line = re.sub(r"\s+", " ", line)
        line = re.sub(r"\s*;\s*", ";", line)
        line = re.sub(r"\s*\(\s*", "(", line)
        line = re.sub(r"\s*\)", ")", line)
        line = re.sub(r"\s*\.\s*", ".", line)

        if line != "":

            if line.startswith(('field ', 'collection ', 'index ')):
                field_def = True
                field_str = ""
            if field_def:
                field_str += line + " "

            if field_def and ";" in line:
                out_lines.append("\t" + field_str.strip().replace("\n", "") + "\n")
                field_str = ""
            elif not field_def:
                if line in ["index_defaults"] or line.startswith(("table ", "view ")):
                    out_lines.append("\n")
                if field_def:
                    line = '\t' + line
                out_lines.append(line + "\n")
                if line in ["table_defaults", "index_defaults"]:
                    out_lines.append("\n")

            if ";" in line:
                field_def = False

    file = open(out_file, mode="w", encoding="utf8")
    file.writelines(out_lines)
    file.close()

def display_usage():
    """
    Displays usage info of ther program to the console.
    """
    print("\nSampleManger structure file formatter.")
    print("\nUsage:")
    print(f"{sys.argv[0]} input_file [output_file]")
    print("")
    print("Program will format input_file and save it as output_file. When output_file is not set,")
    print("input_file will be overwritten by formated structure.")

if __name__ == "__main__":
    main()
 