# Gets content of file
# Input requires file stored in tests folder and with .plz extension
def get_input():
  try:
    file = input('Filename: ')
    file = 'tests/' + file + '.plz'
    with open(file, 'r') as myfile:
        s = myfile.read()
  except EOFError:
      exit()
  if not file: exit()

  return s
