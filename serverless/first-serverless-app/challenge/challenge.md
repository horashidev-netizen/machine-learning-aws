Our test servers will transmit a JSON object, containing the emoji_type identification element and a random message, to your Lambda function. Example:
{
"emoji_type": 0,
"message": "I love the park"
}

Update the Lambda function by using the following rules:

 emoji_type = 0, returns feeling: "positive"
 emoji_type = 1, returns feeling: "neutral"
 emoji_type = any other value than 0 and 1, returns feeling: "negative"
  
After the previous updates, your Lambda function must return the interpreted sentiment in the following JSON format (as it already does):
{
	"feeling": "positive",
	"message": "I love the park"
}
The validation code will look for a similar output as displayed above. Any extra characters in the output will fail the validation.
 
 Hints:
 Based on the sample code provided (the sample_code.py file that you downloaded in the Practice section): 
 - Update the if-else block to add a variable for the feeling attribute (positive, neutral, negative).
 - The feeling attribute (positive, neutral, negative) is case sensitive.
 - Change the response section of the code to add the feeling attribute instead of custom_message.
 - You must click Deploy to save your code changes.