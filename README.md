                                                                       Home Assignment.
                                                                       
                                                                       
                                                                       
          The main logic of the implementation is :
          Holding a dictionary called keywords, which consists of - 
          keys: time in seconds, 
          value: dictionary looks like -
                {
                  'checkpoint': number of 'checkpoint' occurence at this second , 
                  'avanan' : ...
                  'email' : ...
                  'security' : ...
                }
          
          first of all 
          the code first of all checks if there is an existing JSON file to load previous data into the keywords dictionary.
          o.w initialize keywords with new dictionary.
          then using flask to create an API with two entries :
            1. events
            2. stats.
            
          events - 
            contains 'post' handler function.
            post function -
            1 - parses the sentence of the post request parameters and split it to a words array.
            2 - counts the occurrence of the keywords in the given sentence. 
            3 - save the current time in seconds.
            4 -uses this second as a key in the keywords dictionary, and add to this key dictionary with the occurrence number of the words.
                  - if there is already a dictionary with data for this second - it just adds the numbers from the current post to the existing dictionary.
                  
            5 - updating the JSON persistency json file.
            
         stats -
          contains 'get' handler function.
          get function - 
          1 - calculates the relevant interval time (which given in the get request).
          2 - initialize an answer dictionary with the keywords as keys and 0 as values.
          3 - for each second in this interval , checks if the keywords dict contains value for this second , 
              if so - adds the relevant values for this second to the answer dictionary.
          
          
          
          
          
          
          
          
          
          
          
            
