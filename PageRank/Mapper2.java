
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


import java.io.IOException;

/*Author: Shaila*/

public class Mapper2 extends Mapper<LongWritable, Text, Text, Text> {
	int i =0;
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        
        /* Parse the data from the result of every previous iteration. Which will sent to 
         * Reducer2 for calculating the PageRank.
         */
        
        int tIdx1 = value.find("\t");
        int tIdx2 = value.find("\t", tIdx1 + 1);
        String page = Text.decode(value.getBytes(), 0, tIdx1);
        String pageRank = Text.decode(value.getBytes(), tIdx1 + 1, tIdx2 - (tIdx1 + 1));
        String links = Text.decode(value.getBytes(), tIdx2 + 1, value.getLength() - (tIdx2 + 1));
        Text pageRankWithTotalLinks;
        String temp = "Home,About,Product,Links";
        String [] temparray =temp.split(",");
        String[] allOtherPages = links.split(",");
        
        for (String otherPage : allOtherPages) {
        	pageRankWithTotalLinks = new Text(pageRank + "\t" + allOtherPages.length);
        	if(otherPage.equals(""))
        	{
        		if(PageRank.nodes.size() <20){
        		otherPage = temparray[i];
        		i++;}
        	
        		
        		
        	}
        	
        	//System.out.println("otherPage " +otherPage);
            //System.out.println("Job2Mapper:  new Text(otherPage) && pageRankWithTotalLinks: " +new Text(otherPage) +" " +pageRankWithTotalLinks);
            
            context.write(new Text(otherPage), pageRankWithTotalLinks); 
            //System.out.println("Job2Mapper:  new Text(otherPage) && pageRankWithTotalLinks: " +new Text(otherPage) +" " +pageRankWithTotalLinks);
            
        }
        
        
        context.write(new Text(page), new Text(PageRank.separator + links));
        //System.out.println("Job2Mapper:  new Tex(Page) && new Text(PageRank.LINKS_SEPARATOR + links: " +new Text(page) +" " +new Text(PageRank.LINKS_SEPARATOR + links));
    }
    
}

