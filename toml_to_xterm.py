import os
import sys

def convert_toml_to_xterm(content):
    res = ""

    while True:
        tag = content.find("[colors.");

        if tag == -1:
            break

        prefix = content[content[tag:].find(".") + tag + 1:content[tag:].find("]") + tag] + "_"
        prefix = prefix.replace('.', '_')
        tag_end = tag + content[tag:].find('\n') + 1;

        if tag_end == -1:
            break

        res += "!" + content[tag:tag_end] + "\n"
        while (True):
            if content[tag_end] == '#':
                tag_end = tag_end + content[tag_end:].find('\n') + 1;
            else:
                break;
        out, last_len = convert(content[tag_end:], prefix)
        res += out
        content = content[len(content) - last_len + 1:]

    return res

def convert(content, prefix):
    res = ""
    while content[0] != '\n' and content[0] != '[':
        if content[0] == '#':
            content = content[content.find('\n') + 1:]

        template = "#define " + prefix
        whitespace = content.find(" ")
        template += content[:whitespace] + " "
        hash = content.find("#")
        template += (19 - len(template)) * " "
        template += content[hash:hash + 7] + "\n"
        content = content[content.find('\n') + 1:]
        res += template
        if len(content) == 0:
            break
    return res, len(content)

def strip_extension(file_name):
    base_name, extension = os.path.splitext(file_name)
    return base_name 

def main():
    input_dir = os.path.join(os.getcwd(), sys.argv[1])
    out = os.path.join(os.getcwd(), "xterm_themes/")
    if not os.path.exists(out):
        os.makedirs(out)

    with open("/home/box/toml_to_xterm/alacritty-theme/themes/catppuccin_frappe.toml", 'r') as file:
        content = file.read()
        theme = convert_toml_to_xterm(content)
        print(theme)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        print(file_path)
        with open(file_path, 'r') as file:
            content = file.read()
            theme = convert_toml_to_xterm(content)
            with open(os.path.join(out, strip_extension(filename)), 'w') as out_file:
                out_file.write(theme)

if __name__ == "__main__":
    main()
