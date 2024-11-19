import os
import sys

def convert_toml_to_uxterm(content):
    res = ""
    tags = ["[colors.primary]", "[colors.cursor]", "[colors.normal]", "[colors.bright]"]
    rows_to_consume = [2, 2, 8, 8]

    for i in range(0, 4):
        res += "!" + tags[i] + "\n"
        pos = content.find(tags[i]);
        if (pos != -1):
            pos = pos + content[pos:].find('\n') + 1;
            res += convert(content[pos:], tags[i][tags[i].find(".") + 1:tags[i].find("]")] + "_", rows_to_consume[i])
    return res

def convert(content, prefix, n_rows):
    res = ""
    while (n_rows != 0):
        template = "#define " + prefix
        whitespace = content.find(" ")
        template += content[:whitespace] + " "
        hash = content.find("#")
        template += (19 - len(template)) * " "
        template += content[hash:hash + 6] + "\n"
        content = content[content.find('\n') + 1:]
        res += template
        n_rows -= 1;
    return res

def strip_extension(file_name):
    base_name, extension = os.path.splitext(file_name)
    return base_name 

def main():
    input_dir = os.path.join(os.getcwd(), sys.argv[1])
    out = os.path.join(os.getcwd(), "uxterm_themes/")
    if not os.path.exists(out):
        os.makedirs(out)


    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        print(file_path)
        with open(file_path, 'r') as file:
            content = file.read()
            theme = convert_toml_to_uxterm(content)
            with open(os.path.join(out, strip_extension(filename)), 'w') as out_file:
                out_file.write(theme)

if __name__ == "__main__":
    main()
