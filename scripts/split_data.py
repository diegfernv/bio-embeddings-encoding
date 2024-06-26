import sys, os, argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from Bio import SeqIO

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", help="Path of the data", required=True)
    parser.add_argument("-f", "--filename", help="Filename using 'vs' nomenclature", required=True)
    parser.add_argument("-o","--output", help ="Output path", required=True)
    parser.add_argument("-g", "--percentage", help="Percentage of data you want to retrieve")
    parser.add_argument("-t", "--task", help="Task, 'binary' or 'classification'", required=False, default='classification')
    args = parser.parse_args()

    if args.task == 'classification':
        classes = args.filename.split("vs")
    elif args.task != 'binary':
        print("Not valid task provided. Exiting...")
        exit(-1)
    
    percentage = int(args.percentage)/100
    
    # The embedding dimension has no usage for the moment.
    models = [
            ("bepler", 121),
            ("cpcprot", 512),
            ("esm", 1280),
            ("esm1b", 1280),
            ("fasttext", 512),
            ("glove", 512),
            ("onehot", 21),
            ("plusrnn", 1024),
            ("prottrans_albert", 4096),
            ("prottrans_bert", 1024),
            ("prottrans_t5bfd", 1024),
            ("prottrans_xlnet_uniref100", 1024),
            ("prottrans_t5xlu50", 1024),
            ("seqvec", 1024),
            ("word2vec", 512)
        ]
    models.extend([(f"Group_{i}", -1) for i in range(8)])
    models.extend([(f"Group_{i}_fft", -1) for i in range(8)])

    df_total = []
    df_benchmark = []
    
    print("[CSV/FASTA] Loading {}/{}".format(args.input, args.filename))
    df_total = pd.read_csv("{}/{}.csv".format(args.input, args.filename))
    
    if args.task == 'classification':
        df_benchmark = df_total.sample(frac=percentage, random_state=42).sort_values(by=['class','index'])
        df_residue = df_total.drop(df_benchmark.index).sort_values(by=['class','index'])
    elif args.task == 'binary':
        df_benchmark = df_total.sample(frac=percentage, random_state=42)
        df_residue = df_total.drop(df_benchmark.index)
    else:
        print("Not valid task provided. Exiting...")
        exit(-1)


    if not os.path.exists("{}/{}".format(args.output, args.filename)):
        Path("{}/{}".format(args.output, args.filename)).mkdir(parents=True) 
    else:
        print("[WARN] {}/{} already exists! Adding new files...".format(args.output, args.filename))


    for model in models:
        for reduced in ["", "_reduced"]:
            # Cargo el primero        

            if( not os.path.exists( "{}/{}/{}{}.npy".format(args.input, args.filename, model[0], reduced)) ):
                continue

            print("[NPY] Loading {}/{}/{}{}.npy".format(args.input, args.filename, model[0], reduced))
            data = np.load("{}/{}/{}{}.npy".format(args.input, args.filename, model[0], reduced))

            # Reduzco
            benchmark = data[df_benchmark.index.to_numpy()]
            residue = data[df_residue.index.to_numpy()]

            print("[NPY] Saving Into {}/{}/benchmark/".format(args.output, args.filename))
            if not os.path.exists("{}/{}/benchmark".format(args.output, args.filename)):
                os.mkdir("{}/{}/benchmark".format(args.output, args.filename)) 
            np.save("{}/{}/benchmark/{}{}.npy".format(args.output, args.filename, model[0], reduced), benchmark)
            
            print("[NPY] Saving Into {}/{}/residue/".format(args.output, args.filename))
            if not os.path.exists("{}/{}/residue".format(args.output, args.filename)):
                os.mkdir("{}/{}/residue".format(args.output, args.filename)) 
            np.save("{}/{}/residue/{}{}.npy".format(args.output, args.filename, model[0], reduced), residue)
    
    
    print("[CSV] Saving into {}/{}/benchmark.csv".format(args.output, args.filename))
    df_benchmark.to_csv("{}/{}/benchmark.csv".format(args.output, args.filename), index=False)
    print("[CSV] Saving into {}/{}/residue.csv".format(args.output, args.filename))
    df_residue.to_csv("{}/{}/residue.csv".format(args.output, args.filename), index=False)

