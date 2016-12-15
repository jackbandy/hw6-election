

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
/*Author: Shaila*/

public class Reducer2 extends Reducer<Text, Text, Text, Text> {
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, 
                                                                                InterruptedException {
        
        /* The PageRank Calculation is done in this class */
        
        String links = "";
        double sum = 0.0;
                
        for (Text value : values) {
 
            String content = value.toString();
            
            if (content.startsWith(PageRank.separator)) {
                
                links += content.substring(PageRank.separator.length());
                //System.out.println("links:"+ links);
            } else {
                
                String[] split = content.split("\\t");
                
                double pageRank = Double.parseDouble(split[0]);
                int totalLinks = Integer.parseInt(split[1]);
                // add the contribution of all the pages having an outlink pointing  to the current node
                	sum += (pageRank / totalLinks);
                	//System.out.println("reduce 2:  sumShareOtherPageRanks:" +sumShareOtherPageRanks);
                
            }

        }
        //calculate the new Rank
        double newRank = PageRank.DampingFact * sum + (1 - PageRank.DampingFact)/PageRank.nodes.size();
        context.write(key, new Text(newRank + "\t" + links));
        // Check if it reaches in the convergence;
        PageRank.convergence +=newRank;
        //System.out.println("############convergence: ########" +PageRank.convergence);
        if((1.0 - PageRank.convergence) < 0.0001){
        	//System.out.println("############Iterations: ########" +PageRank.runs);
        	PageRank.runs = 101;
        	}
        
        //System.out.println("Rejucer2:    key*****"+ key +"    newpageRank: " + newRank);
        
        
    }

}
