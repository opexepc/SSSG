# SSS Genegator
import sys

VERSION = "0.0.2"

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

MAX_ALLOCATION_SIZE_TAG  = "@s"
max_allocation_size = "100000"

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

def gen_allocator(file_out, type, name, count):
  file_out.write("\n\tif(" + count + " < 0) goto fail;\n")
  file_out.write("\t__size = sizeof(" + type + ") * " + count + ";\n")
  file_out.write("\tif(__size > " + max_allocation_size + ")\n\t\tgoto fail;\n")
  file_out.write("\ts->" + name + " = (" + type + "*)malloc(__size);\n")
  file_out.write("\tif(!s->" + name + ") goto fail;\n")

def gen_version_check(file_out):
  file_out.write("\tint new_version;\n\n")
  file_out.write("\tif(SSS_read_i32(f, &new_version)) return 1;\n")
  file_out.write("\tif(new_version != __version)\n\t{\n\t\tif(version)\n\t\t\t*version = new_version;\n\t\treturn SSS_BROKEN_VERSION;\n\t}\n\n")

# write function on sample
def gen_func(file_out, func_name, struct_name, version, fields, patterns):
  # function declaration
  file_out.write("\nstatic int SSS_" + func_name +"_" + struct_name + "(FILE *f, " + struct_name + " *s")
  if func_name == "read":
    file_out.write(", int *version")
  file_out.write(")\n{\n")
  
  file_out.write("\tconst int __version = " + str(version) + ";\n")

  if func_name == "write":
    file_out.write("\tif(SSS_write_i32(f, &__version)) return 1;\n\n")
  elif func_name == "read":
    gen_version_check(file_out)
    file_out.write("\tsize_t __size = 0;\n")
    file_out.write("\tmemset(s, 0, sizeof(" + struct_name + "));\n\n")

  need_free = []
  # write all founded structure fields to patterns
  for field in fields:
    condition = field[2]
    condition = condition.replace("$func", func_name)
    condition = condition.replace("$name", field[1])

    value_type = 0
    var_type = field[0]
    var_name = field[1]
    var_size = field[3]


    if var_size == '*':
      value_type = 1
    elif var_size != "":
      value_type = 2

    if value_type == 1:
      condition = condition.replace('&', "")
      if func_name == "read":
        gen_allocator(file_out, var_type, var_name, "1")
        need_free.append(var_name)
    # if need loop
    elif value_type == 2:

      if not(var_size.isdigit()):
        if func_name == "read":
          gen_allocator(file_out, var_type, var_name, var_size)
          need_free.append(var_name)

      file_out.write("\n\tfor(int i = 0; i < " + var_size + "; ++i)\n\t{\n")
      condition = condition.replace(field[1], field[1] + "[i]")

    conditions = list(map(str.strip, condition.split('\n')))
    for cds in conditions:
      if value_type == 2:
        file_out.write("\t")
      file_out.write("\tif(" + cds + ") goto fail;\n")

    if value_type == 2:
      file_out.write("\t}\n")

  file_out.write("\n\tgoto success;\n\n")

  file_out.write("fail:\n")
  for i in need_free:
    file_out.write("\tif(s->" + i + ")\n\t{\n\t\tfree(s->" + i + ");\n\t\ts->" + i + " = NULL;\n\t}\n")
  file_out.write("\treturn 1;\n")

  file_out.write("\nsuccess:\n")
  file_out.write("\treturn 0;\n}\n")

def sssg(in_path, out_path, patterns):
  file_in = open(in_path, "r")
  file_out = open(out_path, "w")

  # name for defines and tags
  name = "SSS_" + in_path[:in_path.find('.')]
  name = name.replace('\\', '_')
  name = name.replace('/', '_')

  file_out.write("// generated with SSSG " + VERSION + "\n")
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

          var_type = tokens[0][:len(ptn[0])]
          if ptn[0] == var_type:
            
            var_name = tokens[1][:-1].replace('*', "")
            var_size = ""

            from_size = line.find('[') + 1
            to_size = line.find(']')

            if line.count('[') != line.count(']'):
              print("set correct size in line: " + line)
              return

            if '*' in line:
              var_size = "*"

            if from_size != 0 and to_size != -1:
              var_name = var_name.split('[')[0]

              if ('*' in line and "@SIZE" in line) or ('*' not in line):
                var_size = line[from_size : to_size]

            fields.append([var_type, var_name, ptn[1], var_size])

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

    elif argv[i] == MAX_ALLOCATION_SIZE_TAG:
      if i + 1 >= argc:
        print("ERR: set max allocation size")
        return 0x05
      else:
        i += 1
        global max_allocation_size
        max_allocation_size = argv[i]

  if in_path == "":
    print("ERR: set input path")
    return 0x06

  if out_path == "":
    print("ERR: set output path")
    return 0x07

  if patterns_path == "":
    print("ERR: set patterns path")
    return 0x08

  # patterns from file
  patterns = get_patterns(patterns_path)

  # add other include patterns
  for i in cmd_includes:
    patterns.append([INCLUDE_TAG, i])

  # gen code
  if patterns != None:
    return sssg(in_path, out_path, patterns)

main()