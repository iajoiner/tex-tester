import json
import re
import tex_tester
def individual_process(code, tex_string, tex_engine = 'latex'):
    math_pattern = re.compile(r'\$\S*\$')
    textgreek_pattern = re.compile(r'\\text[A-Z]\S*')
    individual_output = {}
    if math_pattern.search(tex_string):
        individual_output['value'] = tex_string[1:-1]
    else:
        individual_output['value'] = tex_string
    if textgreek_pattern.search(tex_string):
        individual_output['tg'] = True
    else:
        individual_output['tg'] = False
    test_res = tex_tester.run_test(tex_string, tex_engine)
    individual_output['text'] = test_res[0]
    individual_output['math'] = test_res[1]
    individual_output['tacc'] = test_res[2]#text accent
    individual_output['macc'] = test_res[3]#math accent
    return individual_output
#Process an array of TeX symbols related to a font
def array_process(array, start = 0, end = 127, tex_engine = 'latex'):    
    code_range = range(start, end + 1)
    output = {}
    for code in code_range:
        output[code] = individual_process(code, array[code - start], tex_engine)
    return output
expanded_dict = {}
with open('/Users/CatLover/Documents/Tex/dvi2tex/symbol_db.json', 'r') as json_file:
    db_dict = json.load(json_file)
    for key in db_dict.keys():
        expanded_dict[key] = array_process(db_dict[key])
    with open('/Users/CatLover/Documents/Tex/dvi2tex/expanded_symbol_db.json', 'w') as new_json_file:
        json.dump(expanded_dict, new_json_file)
