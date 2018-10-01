# spiderman
steam crawling exercise.
ideas:
  1. using requests to visit 'https://store.steampowered.com/search/?'
  2. go to each page individually, find 
                    title,
                    date,
                    rating,
                    popularity,
                    price,
                    publisher,
                    developers,
                    populartag,
                    genre,
 3. use pandas to clean the requested page, convert genre and popular tags to one hot variable
 
 issues: 
 1. Some foreign games might contain illegible characters
      use simple algorithms to remove special characters
 2. Agecheck
      physically visit the page to get the cookie
 
 
 
    
            
