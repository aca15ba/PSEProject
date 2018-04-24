import sheffield.EasyReader;

/*
 * BeanMachine.java  	1.0 12/02/2016
 *
 * Copyright (c) Babatunde Adeola 2016
 */
// This is for a long line error for java which is set at a 100 characters according to the Google Java style Guide.
/** 
* BeanMachine.java
* 
* 
* @version 1.0 12/02/2016
* 
* @author Babatunde Adeola
*/
public class BeanMachine {
    static final ImmutableList<String> NAMES = ImmutableList.of("Ed", "Ann");

// This is for a long line error for java which is set at a 100 characters according to the Google Java style Guide.
	public static void main(String[] args) {
		
		//declare variables
		int Balls;
		int buckets;
		final int _MAX_BALLS = 100;
		final double MAX_BUCKETS_ = 20;
		final int COUNTs = 100;

		int intArray[];    //declaring array
		String[] myStringArray = new String[3];
		
		//ask for No. of balls and buckets
		//ask again if outside range
		do{
		EasyReader keyboard = new EasyReader(); //to read from keyboard
		balls = keyboard.readInt("Enter Number of balls to be dropped");
		buckets = (keyboard.readInt("Enter Number of buckets")-1);
		
		//check the value entered re-request if invalid
		if (balls >MAX_BALLS || buckets >MAX_BUCKETS) {
			//set maximum values for ball and buckets
			System.out.println("Maximum balls = 100 and maximum buckets = 20");
			}
		//reject negative values
		if (balls < 1 || buckets < 1 ){
			System.out.println("Enter a number greater than Zero");
		}
		
		}while(balls > MAX_BALLS || balls < 1 || buckets >MAX_BUCKETS || buckets < 1);
		
		//create an array to represent the number of buckets
		int [] bucket = new int [buckets + 1];
		
		//string to represent direction
		String turn;
		System.out.println("Path taken by each ball");
		
		//loop to pass all balls through bean machine
		for(int i = 0; i < balls; i++) {
			
			int finalBucket = 0; //is to represent final bucket number
			
			//loop for each ball to pass through multiple pins
			for(int j = 0; j < buckets; j ++){
				
				//randomize direction 50/50 L/R
				int choiceDirection = (int)(Math.random() * 2);
				finalBucket += choiceDirection;
				if (choiceDirection == 0)
					turn = "L";
				else
					turn = "R";
				//print out path of ball
				System.out.print(turn);
			}
			//add 1 to value in final bucket to increase number of balls
			bucket[finalBucket]++;
			System.out.println();
		}
		
		//calculate the mean bucket
		double multiply = 0.0;
		for(int i = 0; i <= buckets; i++) {
	    	multiply += (bucket[i]*(i+1));
	    }
		double mean = multiply / balls;
		
		//calculate the modal bucket
		int modalBucket = 0;
		int test = 0;
		for(int i = 0; i <= buckets; i++) {
	    	if (bucket[i] > test){
	    		test = bucket[i];
	    		modalBucket = i+1;
	    	}
	    }
		
		//print ball distribution
		System.out.println("Distribution of balls");
		
		//create a string array to help print distribution
	    String[] ball = new String[buckets + 1];
	    
	    //loop through number of balls
	    for (int i = balls; i > 0; i--) {
	    	//loop through number of buckets
	        for (int j = 0; j <= buckets; j++) {
	        	//print * if its a ball
	            if (i == bucket[j]) {
	                ball[j] = "*";
	                bucket[j]--;}
	            else if (i >1){
	            	ball[j] = " ";
	            }
	            //print _ if its an empty bucket
	            else
	                ball[j] = "_";
	            System.out.print(ball[j]);
	        }
	        System.out.println();
	    }
	    
	    //print modal and mean buckets.
	    System.out.println("The modal bucket is " + modalBucket);
	    System.out.println("The mean bucket is " + mean);
	}
}

public class primitiveParameters
{
	public static void main(String[] args)
	{	go();
	}

	public static void go()
	{	int x = 3;
		int y = 2;
		System.out.println("In method go. x: " + x + " y: " + y);
		falseSwap(x,y);
		System.out.println("in method go. x: " + x + " y: " + y);
		moreParameters(x,y);
		System.out.println("in method go. x: " + x + " y: " + y);
	}

	public static void falseSwap(int x, int y)
	{	System.out.println("in method falseSwap. x: " + x + " y: " + y);
		int temp = x;
		x = y;
		y = temp;
		System.out.println("in method falseSwap. x: " + x + " y: " + y);
	}

	public static void moreParameters(int a, int b)
	{	System.out.println("in method moreParameters. a: " + a + " b: " + b);
		a = a * b;
		b = 12;
		System.out.println("in method moreParameters. a: " + a + " b: " + b);
		falseSwap(b,a);
		System.out.println("in method moreParameters. a: " + a + " b: " + b);
	}
}
