# Bio Embeddings Encoding
This project utilizes the bio-embeddings library for processing biological sequences.

To effectively utilize this project, ensure your directory structure follows the specified order:
```
.
├── run_encoding.sh
├── scripts
│   └── *.py
└── data
    ├── *.fasta
    └── *.csv
```
After adding the necessary .fasta files, encode the data using the following command:
```
./run_encoding.sh ./data sequence
```
Assuming dna.fasta and rna.fasta are provided, executing this script will generate the following files for each listed encoder:
```
.
├── *.sh
├── scripts
│   └── *.py
└── data
    ├── dna
    │    ├── bepler
    │    ├── cpcprot
    │    ├── *
    │    └── esm1b
    ├── dna.fasta
    ├── rna
    │    ├── bepler
    │    ├── cpcprot
    │    ├── *
    │    └── esm1b
    └── rna.fasta
```
Once encoding is completed, add the following directories: output, merged, split, and train:
```
.
├── *.sh
├── scripts
│   └── *.py
└── data
│   ├── *.fasta
│   └── *.csv
└── output
    ├── merged
    ├── split
    └── train
```
Next, execute the script to generate the training data:
```
./generate_data.sh ./data
```
This will create various directories. Assuming dna and rna sequences are provided, the output should resemble the following structure:
```
.
├── *.sh
├── scripts
│   └── *.py
└── data
│   ├── dna
│   │    ├── bepler
│   │    ├── cpcprot
│   │    ├── *
│   │    └── esm1b
│   ├── dna.fasta
│   ├── rna
│   │    ├── bepler
│   │    ├── cpcprot
│   │    ├── *
│   │    └── esm1b
│   └── rna.fasta
└── output
    ├── merged
    │     ├── dnavsrna.csv
    │     └── dnavsrna
    │           ├── bepler
    │           ├── cpcprot
    │           ├── *
    │           └── esm1b
    ├── split
    │     └── dnavsrna
    │            ├── benchmark
    │            │      ├── bepler
    │            │      ├── cpcprot
    │            │      ├── *
    │            │      └── esm1b  
    │            └── residue
    │            │      ├── bepler
    │            │      ├── cpcprot
    │            │      ├── *
    │            │      └── esm1b
    │            ├── benchmark.csv
    │            └── residue.csv
    └── train
          └── dnavsrna
                ├── X_test_onehot.npy
                ├── y_test_onehot.npy
                ├── *
                └── y_val_onehot.npy
```
