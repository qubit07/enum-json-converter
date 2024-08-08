import re
import json
import argparse

def parse_enum_file(file_path):
    enums = {}
    
    with open(file_path, 'r') as file:
        content = file.read()

        # Regular Expression to match C# enum blocks
        enum_blocks = re.findall(r'enum\s+(\w+)\s*{([^}]*)}', content, re.MULTILINE)
        
        for enum_name, enum_body in enum_blocks:
            # Remove comments and extra whitespaces, then split by commas
            enum_members = [member.strip() for member in re.split(r',\s*', enum_body.strip()) if member]
            
            enum_dict = {}
            value = 0
            for member in enum_members:
                # Match name and optional assigned value (decimal or hex)
                match = re.match(r'(\w+)\s*(=\s*(0x[\da-fA-F]+|-?\d+))?', member)
                if match:
                    name = match.group(1)
                    if match.group(3):
                        # Convert the value from hex or decimal to an integer
                        value = int(match.group(3), 0)  # Automatically detects hex (0x) or decimal
                    enum_dict[name] = value
                    value += 1  # Increment value automatically if not assigned
            
            enums[enum_name] = enum_dict
    
    return enums

def write_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Convert C# enums to JSON.')
    parser.add_argument('input_file', type=str, help='Path to the input C# file.')
    parser.add_argument('output_file', type=str, help='Path to the output JSON file.')

    args = parser.parse_args()

    # Process the files
    enum_data = parse_enum_file(args.input_file)
    write_json(enum_data, args.output_file)
    print(f"JSON file '{args.output_file}' successfully created.")

if __name__ == "__main__":
    main()
