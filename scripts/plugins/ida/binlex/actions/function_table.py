from lib import IDA
from gui import GradientTable
from lib import Worker

def process(function_names, functions: list):
    print(f'[-] collecting function data...')
    data = []
    for function in functions:
        chromosome = function.chromosome()
        row = [
            str(hex(function.address())),
            function_names[function.address()],
            'function',
            function.contiguous(),
            function.size(),
            function.number_of_blocks(),
            function.cyclomatic_complexity(),
            function.average_instructions_per_block(),
            function.chromosome_minhash_ratio() or '',
            chromosome.minhash() if chromosome else '',
            function.chromosome_tlsh_ratio() or '',
            chromosome.tlsh() if chromosome else '',
            chromosome.pattern() if chromosome else '',
        ]
        data.append(row)
    return data

def complete(data: list):
    print(f'[*] completed processing functions')
    form = GradientTable(
        data,
        [
            'Address',
            'Name',
            'Type',
            'Contiguous',
            'Size',
            'Number of Blocks',
            'Cyclomatic Complexity',
            'Average Instructions Per Block',
            'Minhash Chromosome Ratio',
            'Chromosome Minhash',
            'TLSH Chromosome Ratio',
            'Chromosome TLSH',
            'Chromosome Pattern'
        ],
        color_column=7,
        min_value=0,
        max_value=1,
        low_to_high=True,
        default_filter_column=1,
        default_sort_column=5,
        default_sort_ascending=False
    )
    form.Show('Binlex Function Table')

def execute(parent):
    if parent.function_table_window:
        return None

    parent.disassemble_controlflow()

    functions = parent.cfg.functions()

    function_names = IDA().get_function_names()

    worker = Worker(
        target=process,
        args=(function_names, functions),
        done_callback=complete
    )
    worker.start()
