import csv
import sys
def main():
  if len(sys.argv) != 2:
        print(sys.argv)
        print("Uso: python ajustar.py <parametro1>")
        sys.exit(1)
  arquivo = sys.argv[1]
  data = []
  with open(arquivo, 'r') as file:
      reader = csv.reader(file)
      next(reader)  # Skip the header
      for row in reader:
          labels = [label.strip() for label in row[0].split(';')]  # Strip whitespace and newline characters
          row_dict = {'ID': labels[0],
                      'Nome': labels[1],
                      'PastaOrigem': labels[2],
                      'PastaDestino': labels[3],
                      'PastaBackup': labels[4]}  # Create dictionary
          data.append(row_dict)

  output_file = 'func_data.csv'
  with open(output_file, 'w', newline='') as file:
      writer = csv.DictWriter(file, fieldnames=['ID', 'Nome', 'PastaOrigem', 'PastaDestino', 'PastaBackup'])
      writer.writeheader()  # Write the header
      writer.writerows(data)  # Write the data rows

if __name__ == "__main__":
    main()