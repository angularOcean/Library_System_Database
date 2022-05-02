from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)

# Routes 

#1. index.html
@app.route('/index.html')
def root():
    return render_template("main.j2")


#2. authors.html
#3. books.html
#4. bookcopies.html
#5. patrons.html
#6. checkouts.html
#7. checkedbooks.html
#8. publishers.html
#9. locations.html

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 