# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import argparse
import csv
import json
import os
import sys

class FileNotFoundError(OSError):
    pass

#Input fields
parser = argparse.ArgumentParser(description='Convert translations from csv to json and vice versa.')
parser.add_argument('-f', '--input_file', metavar="file", type=str, required=True, help='the input csv or json file path - ex. foo.csv')
parser.add_argument('-o', '--output_file', metavar="output", type=str, required=False, help='the output csv or json file [Default: output.json/csv]')
parser.add_argument('-a', '--fill_json_keys', action='store_true', help='json output inserts value into outer keys [Default: empty keys]')

args = parser.parse_args()
DEFAULT_OUTPUT_JSON = 'translations.json'
DEFAULT_OUTPUT_CSV = 'translations.csv'
file_extension = os.path.splitext(args.input_file)[1]

#Validation
if file_extension != ".json" and file_extension != ".csv":
  print("Input file extension must be .json or .csv")
  sys.exit()
if args.output_file:
  if args.input_file == args.output_file:
    print("Output file cannot have the same name as the input file")
    sys.exit()
  output_file_extension = os.path.splitext(args.output_file)[1]
  if output_file_extension != ".json" and output_file_extension != ".csv":
    print("Output file extension must be .json or .csv")
    sys.exit()
  elif file_extension == ".json" and output_file_extension == ".json":
    print("Output file extension must be .csv")
    sys.exit()
  elif file_extension == ".csv" and output_file_extension == ".csv":
    print("Output file extension must be .json")
    sys.exit()

short_lang = {
  'English' : 'en',
  'Vietnamese' : 'vi',
  'Turkish': 'tr',
  'Thai': 'th',
  'Tamil': 'ta',
  'Tagalog': 'tl',
  'Swedish': 'sv',
  'Español': 'es',
  'Russian': 'ru',
  'Punjabi': 'pa',
  'Brazilian Portuguese': 'pt',
  'Norwegian': 'no',
  'Malay': 'ms',
  'Korean': 'ko',
  'Khmer': 'km',
  'Japanese': 'ja', 
  'Italian': 'it',
  'Indonesian': 'id', 
  'Hindi': 'hi', 
  'Creole': 'ht', 
  'German': 'de', 
  'French': 'fr', 
  'Finnish': 'fi', 
  'Dutch': 'nl', 
  'Danish': 'da', 
  'Simplified Chinese': 'zh',
  'Burmese': 'my'
}
long_lang = {short: long for long, short in short_lang.items()}

#Convert csv to json
if file_extension == ".csv":
  try:
    with open(args.input_file) as f:
      with open(args.output_file or DEFAULT_OUTPUT_JSON, 'w') as output_file:
        reader = csv.DictReader(f)
        rows = list(reader)
        output_file.write("{\n")
        for i in range(len(rows)):
          row = rows[i]
          if args.fill_json_keys:
            output_file.write("  \"%s\": {\n" % i)
          else:
            output_file.write("  \"\": {\n")
          is_first_print = True
          for lang in row:
            value = row[lang].strip().replace("\n", "\\n").replace("\t", "\\t")
            if is_first_print:
              output_file.write("    \"{}\": \"{}\"".format(short_lang[lang], value))
              is_first_print = False
            else:
              output_file.write(",\n    \"{}\": \"{}\"".format(short_lang[lang], value))
          if i != len(rows) - 1:
            output_file.write("\n  },\n")
          else:
            output_file.write("\n  }\n")
        output_file.write("}\n")
  except FileNotFoundError:
    print("Cannot find given input file")
#Convert json to csv
elif file_extension == ".json":
  try:
    with open(args.input_file) as f:
      with open(args.output_file or DEFAULT_OUTPUT_CSV, 'w') as output_file:
        translation_dict = json.load(f)
        en_translations = ([translation_dict for label in translation_dict.keys()])
        first_key = list(translation_dict.keys())[0]
        headers = ([long_lang.get(lang) for lang in translation_dict.get(first_key)])
        header_map = {}
        for header in headers:
          header_map[short_lang.get(header)] = list()
        content = [translation_dict.get(key) for key in translation_dict.keys()]
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(headers)
        # Organizes the translations so that this script still works if 
        # each json translation is in a different order (less efficient but less error prone)
        for translation in content:
          for t_val in translation:
            header_map[t_val].append(translation.get(t_val))
        for i in range(len(header_map.get("en"))):
          row = []
          for header in header_map:
              row.append(header_map.get(header)[i])
          csv_writer.writerow(row)
  except FileNotFoundError:
    print("Cannot find given input file")