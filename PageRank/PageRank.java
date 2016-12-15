

import java.io.IOException;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.HashSet;
import java.util.Set;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.Job;

/*Author: Shaila*/


public class PageRank {
    
    
	public static Double DampingFact = 0.4;
    public static int MaxIterations = 100;
    public static String InputPath = "";
    public static String OutputPath = "";
    public static int runs;
    public static double convergence;
    public static NumberFormat nf = new DecimalFormat("00");
    public static Set<String> nodes = new HashSet<String>();
    public static String separator = "|";
    
    
    /**
     * This is the main class run in Hadoop and our programm will start form here.
     */
    public static void main(String[] args) throws Exception {
        
        
            // parse input parameters
            for (int i = 0; i < args.length; i += 2) {
               
                String key = args[i];
                String value = args[i + 1];
                PageRank.InputPath = key;
                PageRank.OutputPath= value;
            
                //System.out.println("key: "+ key + "Value:" + value);
                
            }
                
        // check for parameters Validity
        if (PageRank.InputPath.isEmpty() || PageRank.OutputPath.isEmpty()) {
            System.out.println("Invalid Input!");
            System.exit(1);
        }
        
        // delete output path if it exists already
        FileSystem fs = FileSystem.get(new Configuration());
        if (fs.exists(new Path(PageRank.OutputPath)))
            fs.delete(new Path(PageRank.OutputPath), true);
        
        Thread.sleep(1000);
        
        String inPath = null;;
        String lastOutPath = null;
        PageRank pagerank = new PageRank();
        
        //Run Job1, Which will parse the weblink graph from the input file and make output file for first iteration.
        System.out.println("Running Job#1............");
        boolean isCompleted = pagerank.job1(InputPath, OutputPath + "/iter00");
        if (!isCompleted) {
            System.exit(1);
        }
        
        // Iterations will run until reach the convergence; 
        //If the convergence is not achieved with in 1000 iteration then it will turn automatically.
        for (runs = 0; runs < MaxIterations; runs++) {
        	convergence =0.0;
            inPath = OutputPath + "/iter" + nf.format(runs);
            lastOutPath = OutputPath + "/iter" + nf.format(runs + 1);
            System.out.println("Running Job#2 [" + (runs + 1) + "/" + PageRank.MaxIterations + "] (PageRank calculation) ...");
            isCompleted = pagerank.job2(inPath, lastOutPath);
            if (!isCompleted) {
                System.exit(1);
            }
        }
        
        //Call job3 which will sort the pages according to PageRank
        System.out.println("Running Job#3.............");
        isCompleted = pagerank.job3(lastOutPath, OutputPath + "/result");
        if (!isCompleted) {
            System.exit(1);
        }
        System.out.println("Total Links:" +nodes.size());
        System.out.println("Please see the result in the ouput file: " + OutputPath + "/resultgraph2");
        System.out.println("DONE!");
        System.exit(0);
    }
    
    /**
     * Job1 is for weblink Graph Parsing.
     * initialize the page rank with initial value.
     * 
     */
    public boolean job1(String in, String out) throws IOException, 
                                                      ClassNotFoundException, 
                                                      InterruptedException {
        
        Job job = Job.getInstance(new Configuration(), "Job #1");
        job.setJarByClass(PageRank.class);
        
        // mapper
        FileInputFormat.addInputPath(job, new Path(in));
        job.setInputFormatClass(TextInputFormat.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setMapperClass(Mapper1.class);
        
        // reducer
        FileOutputFormat.setOutputPath(job, new Path(out));
        job.setOutputFormatClass(TextOutputFormat.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.setReducerClass(Reducer1.class);
        
        return job.waitForCompletion(true);
     
    }
    
    /**
     * Job2 is for PageRank Calculation.
     */
    public boolean job2(String in, String out) throws IOException, 
                                                      ClassNotFoundException, 
                                                      InterruptedException {
        
        Job job = Job.getInstance(new Configuration(), "Job #2");
        job.setJarByClass(PageRank.class);
        
        //mapper
        FileInputFormat.setInputPaths(job, new Path(in));
        job.setInputFormatClass(TextInputFormat.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setMapperClass(Mapper2.class);
        
        //reducer
        FileOutputFormat.setOutputPath(job, new Path(out));
        job.setOutputFormatClass(TextOutputFormat.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.setReducerClass(Reducer2.class);

        return job.waitForCompletion(true);
        
    }
    
    /**
     * Job3 is for Ordering the pages according to the Pagerank.
     */
    public boolean job3(String in, String out) throws IOException, 
                                                      ClassNotFoundException, 
                                                      InterruptedException {
        
        Job job = Job.getInstance(new Configuration(), "Job #3");
        job.setJarByClass(PageRank.class);
        
        // mapper
        FileInputFormat.setInputPaths(job, new Path(in));
        job.setInputFormatClass(TextInputFormat.class);
        job.setMapOutputKeyClass(DoubleWritable.class);
        job.setMapOutputValueClass(Text.class);
        job.setMapperClass(Mapper3.class);
        
        // output
        FileOutputFormat.setOutputPath(job, new Path(out));
        job.setOutputFormatClass(TextOutputFormat.class);
        job.setOutputKeyClass(DoubleWritable.class);
        job.setOutputValueClass(Text.class);

        return job.waitForCompletion(true);
        
    }
    
    
    
}