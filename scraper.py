files = ["compose.yml",
"Dockerfile",
"./foodfacts/cli.py",
"./foodfacts/commands/help.py",
"./foodfacts/commands/list.py",]

output_file = "scr.txt"

try:
    with open(output_file, "w") as out:
        for file in files:
            try:
                with open(file, "r") as f:
                    # Write the file header
                    out.write(f"#{file}\n")
                    # Write the file content
                    out.writelines(f.readlines())
                    out.write("\n")  # Add a newline after each file's content
            except FileNotFoundError:
                out.write(f"#{file}\n# File not found\n\n")
    print(f"Contents have been written to {output_file}.")
except Exception as e:
    print(f"An error occurred: {e}")
