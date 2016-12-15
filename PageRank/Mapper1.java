
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
/*Author: Shaila*/




import java.io.IOException;

public class Mapper1 extends Mapper<LongWritable, Text, Text, Text> {
    
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        
        /*
         * Input format is like: <fromlink>	<tolinks>
         * Links are "," separated. 
         * */
        // If there is any line in the input file starts with #, we count that as comment;
    	if (value.charAt(0) != '#') {
            
            int tabIndex = value.find("\t");
            String nodeA = Text.decode(value.getBytes(), 0, tabIndex);
            String links = Text.decode(value.getBytes(), tabIndex + 1, value.getLength() - (tabIndex + 1));
             String[] alllinks = links.split(",");
            for (String nodeB : alllinks) {
            context.write(new Text(nodeA), new Text(nodeB));
            //add the target node to the list.
            PageRank.nodes.add(nodeB);
            //for debuging
            //System.out.println(new Text(nodeA)+" test " +new Text(nodeB));
            }
           // add the current source node to the node list.
           PageRank.nodes.add(nodeA);
                        
        }
 
    }
    
}
