#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import shutil
import os, time, sys

def llda(input_file_name="TopicTermtop5.csv"):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    APP_BATCH = os.path.join(APP_ROOT, 'batch')
    FILE_PATH = os.path.join(APP_ROOT, 'data')
    OUT_PATH = os.path.join(APP_ROOT, 'out2')

    SUMMARY_PATH = os.path.join(OUT_PATH, '01000/summary.txt')
    LABEL_INDEX_PATH = os.path.join(OUT_PATH, '01000/label-index.txt')
    DIS_PATH = os.path.join(OUT_PATH, 'document-topic-distributions.csv')
    
    file_p = os.path.join(FILE_PATH, input_file_name)

    script_name = "script.scala"
    input_name = file_p
    output_dir = "out2"
    shutil.rmtree(output_dir, ignore_errors=True)
    write_script(input_name, output_dir, script_name)
    command = "jre1.7.0_80/bin/java -jar tmt-0.4.0.jar %s" % script_name

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    for line in iter(process.stdout.readline, ''):
        print(line)

    shutil.copyfile(SUMMARY_PATH, FILE_PATH+'/summary.txt')
    shutil.copyfile(DIS_PATH, FILE_PATH+'/document-topic-distributions.csv')
    shutil.copyfile(LABEL_INDEX_PATH, FILE_PATH+'/label-index.txt')
    os.popen('rm data/'+input_file_name+'.term-counts.cache*')


    return 0


def write_script(input, output, file):
    script = """\
    // Stanford TMT Example 6 - Training a LabeledLDA model
    // http://nlp.stanford.edu/software/tmt/0.4/

    // tells Scala where to find the TMT classes
    import scalanlp.io._;
    import scalanlp.stage._;
    import scalanlp.stage.text._;
    import scalanlp.text.tokenize._;
    import scalanlp.pipes.Pipes.global._;

    import edu.stanford.nlp.tmt.stage._;
    import edu.stanford.nlp.tmt.model.lda._;
    import edu.stanford.nlp.tmt.model.llda._;

    val source = CSVFile("%s") ~> IDColumn(1);

    import scala.io.Source
    val listOfLines = Source.fromFile("stopwords.txt").getLines.toList
    val ll = listOfLines.map( x => x.stripLineEnd )

    val tokenizer = {
      SimpleEnglishTokenizer() ~>            // tokenize on space and punctuation
      CaseFolder() ~>                        // lowercase everything
      WordsAndNumbersOnlyFilter() ~>         // ignore non-words and non-numbers
      MinimumLengthFilter(3)                 // take terms with >=3 characters
    }

    val text = {
      source ~>                              // read from the source file
      Column(3) ~>                           // select column containing text
      TokenizeWith(tokenizer) ~>             // tokenize with tokenizer above
      TermCounter() ~>                       // collect counts (needed below)
      TermMinimumDocumentCountFilter(10) ~>   // filter terms in <4 docs
      TermStopListFilter(ll) ~>
      TermDynamicStopListFilter(30) ~>       // filter out 30 most common terms
      DocumentMinimumLengthFilter(10)         // take only docs with >=5 terms
    }

    // define fields from the dataset we are going to slice against
    val labels = {
      source ~>                              // read from the source file
      Column(2) ~>                           // take column two, the year
      TokenizeWith(WhitespaceTokenizer()) ~> // turns label field into an array
      TermCounter() ~>                       // collect label counts
      TermMinimumDocumentCountFilter(10)     // filter labels in < 10 docs
    }

    val dataset = LabeledLDADataset(text, labels);

    // define the model parameters
    val modelParams = LabeledLDAModelParams(dataset);

    // Name of the output model folder to generate
    val modelPath = file("%s");
    // Trains the model, writing to the given output path
    TrainCVB0LabeledLDA(modelParams, dataset, output = modelPath, maxIterations = 1000);
    // or could use TrainGibbsLabeledLDA(modelParams, dataset, output = modelPath, maxIterations = 1500);
    """
    script_c = script % (input, output)
    with open(file, 'w') as fout:
        fout.writelines(script_c)

def helper():
    print sys.argv[0] + " input_file_name"
    sys.exit(1)

def run():
    start_time = time.time()
    llda(input_file_name=sys.argv[1])
    end_time = time.time()
    print("*********LLDA Run Duration:" + str(end_time - start_time))

if __name__ == "__main__":
    if len(sys.argv) != 2:
      helper()
    run()

