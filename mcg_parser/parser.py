import json
import ply.lex as lex
import ply.yacc as yacc

# Step 1: Load tokens from JSON file
with open('./config/keywords.json', 'r') as f:
    tokens_config = json.load(f)

# Step 2: Define the lexer
tokens = (
    'BLOCK',
    'NAME',
    'DESCRIPTION',
    'EXPECTEDRESULT',
    'DELAY',
    'REPEAT',
    'TIMERID',
    'TIMERDURATION',
    'PIN',
    'TRIGGER',
    'CLOCKFREQUENCY',
    'DUTYCYCLE',
    'ARGUMENTS',
    'NUMBER',
    'STRING'
)

# Regular expressions for token definitions
t_BLOCK = tokens_config['tokens']['BLOCK']
t_EXPECTEDRESULT = tokens_config['tokens']['EXPECTEDRESULT']
t_DELAY = tokens_config['tokens']['DELAY']
t_REPEAT = tokens_config['tokens']['REPEAT']
t_TIMERID = tokens_config['tokens']['TIMERID']
t_TIMERDURATION = tokens_config['tokens']['TIMERDURATION']
t_PIN = tokens_config['tokens']['PIN']
t_TRIGGER = tokens_config['tokens']['TRIGGER']
t_CLOCKFREQUENCY = tokens_config['tokens']['CLOCKFREQUENCY']
t_DUTYCYCLE = tokens_config['tokens']['DUTYCYCLE']
t_DESCRIPTION = tokens_config['tokens']['DESCRIPTION']
t_ARGUMENTS = tokens_config['tokens']['ARGUMENTS']
t_NAME = r'[A-Za-z_][A-Za-z0-9_]*'
t_NUMBER = r'\d+'
t_STRING = r'".*?"'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Step 3: Define the parser
class Block:
    def __init__(self, block_type, name, attributes):
        self.block_type = block_type
        self.name = name
        self.attributes = attributes

    def __repr__(self):
        return f"Block(type={self.block_type}, name={self.name}, attributes={self.attributes})"

parsed_blocks = []

def p_block(p):
    '''block : BLOCK NAME
             | BLOCK NAME DESCRIPTION
             | BLOCK NAME EXPECTEDRESULT
             | BLOCK NAME DELAY NUMBER
             | BLOCK NAME REPEAT NUMBER
             | BLOCK NAME TIMERID NUMBER
             | BLOCK NAME TIMERDURATION NUMBER
             | BLOCK NAME PIN NAME
             | BLOCK NAME TRIGGER NAME
             | BLOCK NAME CLOCKFREQUENCY NAME
             | BLOCK NAME DUTYCYCLE NUMBER
    '''
    attributes = {}

    if len(p) == 3:  # BLOCK NAME
        pass
    elif len(p) == 4:  # BLOCK NAME DESCRIPTION
        attributes['Description'] = p[3]
    elif len(p) == 5:  # BLOCK NAME EXPECTEDRESULT or DELAY
        attributes['ExpectedResult'] = p[4]
    elif len(p) == 6:  # BLOCK NAME DELAY NUMBER
        attributes['Delay'] = p[4]
    elif len(p) == 6:  # BLOCK NAME REPEAT NUMBER
        attributes['Repeat'] = p[4]
    elif len(p) == 6:  # Other attributes
        attributes[p[3]] = p[4]

    block_type = p[1]
    name = p[2]
    parsed_blocks.append(Block(block_type, name, attributes))

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Step 4: Input Processing
def parse_input(input_string):
    lexer.input(input_string)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    parser.parse(input_string)

# Example Input
input_string = """
Block: TestCase
  Name: Test Addition
  Description: "Test basic addition function"
  ExpectedResult: 15
Block: TimingControl
  Name: Delay LED
  Delay: 500ms
  Repeat: 5
"""

# Run the parser
parse_input(input_string)

# Generate and print final output
def generate_output(parsed_blocks):
    output = []
    for block in parsed_blocks:
        if block.block_type == 'TestCase':
            output.append(f"TestCase: {block.name} Description: {block.attributes.get('Description')} ExpectedResult: {block.attributes.get('ExpectedResult')}")
        elif block.block_type == 'TimingControl':
            output.append(f"TimingControl: {block.name} Delay: {block.attributes.get('Delay')} Repeat: {block.attributes.get('Repeat')}")

    return "\n".join(output)

final_output = generate_output(parsed_blocks)
print(final_output)