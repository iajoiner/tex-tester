import subprocess
import os
import re
ALL_ENGINES = ['tex','latex','pdftex','pdflatex','xetex','xelatex','luatex','lualatex']
ENGINES_USING_LATEX = ['latex','pdflatex','xelatex','lualatex']
USES_LATEX = {'tex': False,'latex': True, 'pdftex': False, 'pdflatex': True, 'xetex': False, 'xelatex': True, 'luatex': False, 'lualatex': True}
def test_default(tex_string, tex_engine = 'latex'):
    if tex_engine not in USES_LATEX or not USES_LATEX[tex_engine]:
        return '\\relax ' + tex_string + '\\bye'
    else:
        return '\\documentclass{article}\\begin{document}' + tex_string + '\\end{document}'
def process(tex_string, mode = 0):
    if mode == 0:#Text
        return tex_string
    elif mode == 1:#Math
        return '$' + tex_string + '$'
    elif mode == 2:#Text{}
        return tex_string + '{}'
    elif mode == 3:#Math{}
        return '$' + tex_string + '{}$'
    else:
        print(f'Unknown mode: {mode}')
        return tex_string
def run_test(tex_string, tex_engine = 'latex', test_mode = False):
    accent_pattern = re.compile(r'\\[`\'^~"Hrvut=.bcdk]$|\\vec$')
    is_accent = False
    if not test_mode:
        filename = 'TEX_TESTING'
    return_codes = [False, False, False, False] #Text, Math, Text Accent, Math Accent
    if accent_pattern.search(tex_string):#Is it an accent?
        is_accent = True
    for i in range(4):
        if i >= 2 and not is_accent:
            break
        completed_tex_string = test_default(process(tex_string, i), tex_engine)
        if test_mode:
            filename = 'TEX_TESTING' + '_' + tex_engine + str(i) 
            with open(filename + '.tex', 'w') as f:
                f.write(completed_tex_string)
        completed_process = subprocess.run([tex_engine, "-jobname=" + filename, "-halt-on-error", "-interaction=nonstopmode", completed_tex_string], capture_output = True)
        code = completed_process.returncode
        try:
            os.remove(filename + '.aux')
        except Exception:
            pass
        if code != 0:
            return_codes[i] = False 
        else:
            return_codes[i] = True
    return return_codes
def run_multiple_engine_test(tex_string, tex_engines = ALL_ENGINES, test_mode = False):
    return_codes = {}
    for engine in tex_engines:
        return_codes[engine] = run_test(tex_string, engine, test_mode)
    return return_codes
        
print(run_multiple_engine_test('\\~'))
#print(run_test(test_multipl('\\ell', )))
