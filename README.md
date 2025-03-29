# CS50 NOTES
#### Video Demo:  <https://youtu.be/jIlJ__vPMXw>
#### Description:

### **idea**:
        i get the idea from daily using needs
    i need to take alot of notes daily on papers,
    or diffrent application on phone or laptop
### **langueges i used**:
        i used miltaple langueges, that are:
            - python that i used flask framework and used to python files
                - application.py file where i make the main progress of my code
                - the helpers.py it is where i define functions that help me to make the application file more compacte and easier to read
            - html to do more than page for
                - the layout file that make the layout ofr all other files " layout.html "
                - the portoflio of the website index.html
                - the add edit and remove pges add.html and edit.html and remove.html
                - and pages for users log in or sign up signin.html and register.html and
                - and page for apology so if an error accourd it tells the user what is that error aplogy.html
            - i used a css file with booststrap to control the style of my pages styles.css
            - used sqlite to make the data base where i stor the the information of the users and there notes and help me to do the edit add rmove functions notes.db
            - used and .ico file to make an icon for the website icon sticky-notes.ico
            - requirment.txt i used this file to make put the libraries i used in my code
                - cs50 library
                - flask library
                - tempfile library
                - Flask Session library
                - requests library
                - functools library
                - os library
### **application.py**:
            i used in it the main code i defined the bata base and
        then defined the rout of sign in that make the person sign in and check his username exiests in the data base and if the user name and the password are match
         and for the register i used the route register to do it and i make sure the the username dont exist in the data base and if the password and the confirmation of the pass word match and if the user fill the three fields
         then for the index route it is used to show the notes that belongs to the user that sow the title and the content of the note that the person added before
         and for the add route it used to add notes to the data batse where the user belongs and it makes the he add notes by title and content as he like
         the edit route it used for editing notes in the data baes where the user belongs and it makes the user select a note from his notes and make him edit the title and the content of the title as the user like
         the remove route is used for make the user able to remove the note he took by using the title of it and he can delete as he like