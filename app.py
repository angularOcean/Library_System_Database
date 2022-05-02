from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)

# Routes 

#1. index.html
#render a navigation bar
@app.route('/index.html')
def root():
    return render_template("main.j2")


#2. authors.html - Jenna
#3. books.html - Herakles
#4. bookcopies.html - Jenna
#5. patrons.html - Herakles
#6. checkouts.html - Jenna
#7. checkedbooks.html - Herakles
#8. publishers.html - Jenna
#9. locations.html - Herakles

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 