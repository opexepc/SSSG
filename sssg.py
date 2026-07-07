# SSS Genegator
import sys

VERSION = "0.0.1"

# cmd arguments
INPUT_FLAG = "-i"
OUTPUT_FLAG = "-o"
PATTERNS_FLAG = "-p"

# tag for C code
SSSG_TAG = "@SSSG"

# tags for pattern file
START_PATTERN_TAG = "@s"
END_PATTERN_TAG = "@e"
# can be used like cmd argument
INCLUDE_TAG = "@i"

# get patterns for paste code
def get_patterns(in_path):
  file_in = open(in_path, "r")

  pts = []
  value = ""

  in_pattern = 0

  for line in file_in:
    tokens = line.split()

    if in_pattern:

      # check end of pattern declaration
      if len(tokens) > 0 and tokens[0] == END_PATTERN_TAG:
        pts.append([key, value.strip()])
        value = ""
        in_pattern = 0
      else:
        value += line

    # check start of pattern declaration
    if len(tokens) > 1 and tokens[0] == START_PATTERN_TAG:
      key = tokens[1]
      in_pattern = 1

    # check includes
    if len(tokens) > 1 and tokens[0] == INCLUDE_TAG:
      pts.append([tokens[0], tokens[1]])
  
  return pts

# write function on sample
def gen_func(file_out, func_name, struct_name, version, fields, patterns):
  # function declaration
  file_out.write("\nstatic int SSS_" + func_name +"_" + struct_name + "(FILE *f, " + struct_name + " *s)\n{\n")
  file_out.write("\tconst int version = " + str(version) + ";\n")

  if func_name == "write":
    file_out.write("\tif(SSS_write_i32(f, &version)) return 1;\n\n")
  elif func_name == "read":
    file_out.write("\tint new_version;\n\n")
    file_out.write("\tif(SSS_read_i32(f, &new_version)) return 1;\n")
    file_out.write("\tif(new_version != version)\n\t\treturn SSS_BROKEN_VERSION;\n\n")

  # write all founded structure fields to patterns
  for field in fields:
    condition = field[2]
    condition = condition.replace("$func", func_name)
    condition = condition.replace("$name", field[1])

    conditions = list(map(str.strip, condition.split('\n')))
    for cds in conditions:
      file_out.write("\tif(" + cds + ") return 1;\n")

  file_out.write("\n\treturn 0;\n}\n")

def sssg(in_path, out_path, patterns):
  file_in = open(in_path, "r")
  file_out = open(out_path, "w")

  # name for defines and tags
  name = "SSS_" + in_path[:in_path.find('.')]
  name = name.replace('\\', '_')
  name = name.replace('/', '_')

  file_out.write("// generated with SSSG\n")
  file_out.write("#ifndef " + name + "\n")
  file_out.write("#define " + name + "\n\n")

  # add all includes in file top
  for ptn in patterns:
    if ptn[0] == INCLUDE_TAG:
      file_out.write("#include \"" + ptn[1] + "\"\n")

  in_struct = 0
  declarated = 0
  struct_name = ""
  version = -1
  # fields for function generator
  fields = []

  for line in file_in:
    tokens = line.split()

    if in_struct:

      # find structure name
      if "typedef" in line:
        if tokens[-1] == '{':
          struct_name = tokens[-2]
        else:
          struct_name = tokens[-1]

      # collect structure fields
      if len(tokens) > 1:
        for ptn in patterns:
          if ptn[0] == tokens[0]:
            fields.append([tokens[0], tokens[1][:-1], ptn[1]])

      # find end of structure
      if '}' in line:
        if version == -1:
          print("set version")
          break

        gen_func(file_out, "read", struct_name, version, fields, patterns)
        gen_func(file_out, "write", struct_name, version, fields, patterns)
        fields = []
        in_struct = 0
        version = -1

    # find SSSG tag
    if SSSG_TAG in line:
      from_ver = line.find('[') + 1
      to_ver = line.find(']')

      if from_ver == 0 or to_ver == -1:
        print("set correct version in file " + in_path)
        break

      version = int(line[from_ver : to_ver])
      if version < 0:
        print("set unsigned version")
        break;
        
      in_struct = 1

  file_out.write("\n#endif // " + name)
  
  return 0x00

def main():
  # get amd arguments
  argv = sys.argv
  argc : int = len(argv)

  in_path = ""
  out_path = ""
  patterns_path = ""

  # other includes from cmd
  cmd_includes = []
  
  # check arguments
  for i in range(argc):

    if argv[i] == INPUT_FLAG:
      if i + 1 >= argc:
        print("ERR: set input path")
        return 0x01
      else:
        i += 1
        in_path = argv[i]

    elif argv[i] == OUTPUT_FLAG:
      if i + 1 >= argc:
        print("ERR: set output path")
        return 0x02
      else:
        i += 1
        out_path = argv[i]

    elif argv[i] == PATTERNS_FLAG:
      if i + 1 >= argc:
        print("ERR: set patterns path")
        return 0x03
      else:
        i += 1
        patterns_path = argv[i]

    # find include and append this like include pattern
    elif argv[i] == INCLUDE_TAG:
      if i + 1 >= argc:
        print("ERR: set include path")
        return 0x04
      else:
        i += 1
        cmd_includes.append(argv[i])

  if in_path == "":
    print("ERR: set input path")
    return 0x05

  if out_path == "":
    print("ERR: set output path")
    return 0x06

  if patterns_path == "":
    print("ERR: set patterns path")
    return 0x07

  # patterns from file
  patterns = get_patterns(patterns_path)

  # add other include patterns
  for i in cmd_includes:
    patterns.append([INCLUDE_TAG, i])

  # gen code
  if patterns != None:
    return sssg(in_path, out_path, patterns)

main()