# Fetch-point-redeem
Fetch Coding Exercise - Software Engineering Internship
What do I need to submit?
Please write a program that reads from a CSV file called transactions.csv in the current working directory, processes an argument, and returns a response based on the conditions outlined in the next section.  You can use any language.  
We must be able to compile and run your code; provide any documentation necessary to accomplish this as part of the code you submit. Please assume the reviewer has not executed a code in your language before when developing your documentation. 
What does it need to do? 
Background 
Our users have points in their accounts. Users only see a single balance in their accounts. But for reporting purposes, we actually track their points per payer. In our system, each transaction record contains: payer (string), points (integer), timestamp (date). 
For earning points, it is easy to assign a payer. We know which actions earned the points. And thus, which partner should be paying for the points. 
When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are spent. There are two rules for determining what points to "spend" first: 
We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received) 
We want no payer's points to go negative. 
We expect your code to
Read the transactions from a CSV file.
Spend points based on the argument using the rules above.
Return all payer point balances.
Example 

1. When you run your program, you will pass in an argument which is the amount of points to spend.
For example, using a Python program to spend 5000 points would look like this:

python3 mycode.py 5000
2. Your code will ingest a CSV file with an example sequence: 
"payer","points","timestamp"
"DANNON",1000,"2020-11-02T14:00:00Z"
"UNILEVER",200,"2020-10-31T11:00:00Z"
"DANNON",-200,"2020-10-31T15:00:00Z"
"MILLER COORS",10000,"2020-11-01T14:00:00Z"
"DANNON",300,"2020-10-31T10:00:00Z"


3. After the points are spent, the output should return the following results: 
{ 
"DANNON": 1000, 
"UNILEVER": 0, 
"MILLER COORS": 5300 
} 

How do I submit it? 
Provide a link to a public repository, such as GitHub or BitBucket, that contains your code to the provided link through Greenhouse.
FAQ 
How will this exercise be evaluated? 
An engineer will review the code you submit. At a minimum they must be able to run the code and the code must provide the expected results. You should provide any necessary documentation within the repository. 
I have questions about the problem statement 
For any requirements not specified via an example, use your best judgment to determine the expected result. 
Can I provide a private repository? 
If at all possible, we prefer a public repository because we do not know which engineer will be evaluating your submission. Providing a public repository ensures a speedy review of your submission. If you are still uncomfortable providing a public repository, you can work with your recruiter to provide access to the reviewing engineer. 

