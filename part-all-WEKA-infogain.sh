java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.1/celeb.arff -o -x 10 > 3.1/DATA-support-vector-machines
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 3.1/celeb.arff -o -x 10 > 3.1/DATA-naive-bayes
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.1/celeb.arff -o -x 10 > 3.1/DATA-decision-trees

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.1/celeb.arff -o -x 10 > 3.1/3.1output.txt

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.2/popstars.arff -o -x 10 > 3.2/DATA-support-vector-machines
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 3.2/popstars.arff -o -x 10 > 3.2/DATA-naive-bayes
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.2/popstars.arff -o -x 10 > 3.2/DATA-decision-trees

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.2/popstars.arff -T 3.2/popstars.arff -o -no-cv > 3.2/3.2output.txt

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.3/news.arff -o -x 10 > 3.3/DATA-support-vector-machines
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 3.3/news.arff -o -x 10 > 3.3/DATA-naive-bayes
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.3/news.arff -o -x 10 > 3.3/DATA-decision-trees

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.4/pop-vs-news.arff -o -x 10 > 3.4/DATA-support-vector-machines
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 3.4/pop-vs-news.arff -o -x 10 > 3.4/DATA-naive-bayes
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.4/pop-vs-news.arff -o -x 10 > 3.4/DATA-decision-trees

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.4/500-pop-vs-news.arff -o -x 10 > 3.4/DATA-500-support-vector-machines
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 3.4/500-pop-vs-news.arff -o -x 10 > 3.4/DATA-500-naive-bayes
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.4/500-pop-vs-news.arff -o -x 10 > 3.4/DATA-500-decision-trees

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.4/500-pop-vs-news.arff -o -x 10 > 3.4/3.4output.txt

java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.4/250-pop-vs-news.arff -o -x 10 > 3.4/DATA-250-support-vector-machines
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 3.4/250-pop-vs-news.arff -o -x 10 > 3.4/DATA-250-naive-bayes
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.4/250-pop-vs-news.arff -o -x 10 > 3.4/DATA-250-decision-trees


sh /u/cs401/WEKA/infogain.sh 3.1/celeb.arff > 3.5/INFO-GAIN-celeb
sh /u/cs401/WEKA/infogain.sh 3.2/popstars.arff > 3.5/INFO-GAIN-popstars
sh /u/cs401/WEKA/infogain.sh 3.3/news.arff > 3.5/3.5output.txt
sh /u/cs401/WEKA/infogain.sh 3.4/pop-vs-news.arff > 3.5/INFO-GAIN-pop-vs-news

