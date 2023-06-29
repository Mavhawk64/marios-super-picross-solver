// Java Program to implement
// the above approach
import java.io.*;
import java.util.*;
public class GFG {
    
    static ArrayList<Integer> nums = new ArrayList<Integer>();
    static ArrayList<Integer> curr = new ArrayList<Integer>();
    static ArrayList<ArrayList<Integer>> ans = new ArrayList<ArrayList<Integer>>();
    static ArrayList<Boolean> visited = new ArrayList<Boolean>();
    
    // Function to fill the vector curr
    // while maintaining the indices visited
    // in the array num
    static void backtrack()
    {
    
    	// If current permutation is complete
    	if (curr.size() == nums.size())
    	{
        	ans.add(curr);
        	for(int i = 0; i < curr.size(); i++)
        	{
        		System.out.print(curr.get(i) +" ");
        	}
        	System.out.println();
    	}
    
    	// Traverse the input vector
    	for (int i = 0; i < (int)nums.size();i++)
    	{
    
    	// If index is already visited
    	if (visited.get(i))
    		continue;
    
    	// If the number is duplicate
    	if (i > 0 && (nums.get(i) == nums.get(i - 1)) && !visited.get(i - 1))
    		continue;
    
    	// Set visited[i] flag as true
    	visited.set(i, true);
    
    	// Push nums[i] to current vector
    	curr.add(nums.get(i));
    
    	// Recursive function call
    	backtrack();
    
    	// Backtrack to the previous
    	// state by unsetting visited[i]
    	visited.set(i, false);
    
    	// Pop nums[i] and place at
    	// the back of the vector
    	curr.remove(curr.size() - 1);
    	}
    }
    // Function to pre-process the vector num
    static ArrayList<ArrayList<Integer>> permuteDuplicates()
    {
    	// Sort the array
    	Collections.sort(nums);
    
    	for(int i = 0; i < nums.size(); i++)
    	{
    	visited.add(false);
    	}
    
    	// Find the distinct permutations of num
    	backtrack();
    
    	return ans;
    
    }
    
    // Function call to print all distinct
    // permutations of the vector nums
    
    static void getDistinctPermutations()
    {
    	ans = permuteDuplicates();
    
    
    }
    
    // Driver code
    public static void main (String[] args)
    {
    
    	// Input
    	nums.add(1);
    	nums.add(2);
    	nums.add(2);
    	nums.add(1);
    
    	// Function call to print
    	// all distinct permutations
    	getDistinctPermutations();
    }
}

// This code is contributed by avanitrachhadiya2155
