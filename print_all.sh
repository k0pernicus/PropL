#DIR is the directory to find files to transform in PDF
DIR=Rslts_propl/
#All files in DIR
FILES=$DIR*

#Transform tex files into pdf
for i in $FILES
do
  pdflatex $i -output-directory=$DIR
done

#Destroy log and aux files
ACT_DIR=./
cd $DIR
rm -Rf *.log *.aux
cd $ACT_DIR
