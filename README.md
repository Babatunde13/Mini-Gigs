## Mini Gigs
This project named Mini-Gigs is a web app where professionals can get jobs and recruiters can employ professionals <br>

To install the dependencies to run this program write `pip install -r requirements.txt` in your terminal<br>

The main directory is the `app` directory which contains all the code for the project <br>
The migrations directory is useful when there's any change in the model like adding columns, or tables just write `flask db migrate` to make migrations <br>

This directory can be describes with the tree like structure below:
mini-gigs----¬
        !   app/---¬
        !           !----templates/---¬
        !           !                 !-all html files
        !           !
        !           !----static/------¬
        !                           !----all css files
        !                           !-----resume/
        !                           !-----profileimages/
        !           !----routes.py (module for view function)
        !           !----models.py (module for creating db models)
        !           !----forms.py (module for flask forms)
        !           !----utils.py (module for creating helper funcions that are used inn other modules)
        !           !----site.db (the development db)
        !---migrations/
        !--app.py (the module that runs the app)
        !--REAFME.txt
        !--requirements.txt (the dependency of the app)
        !--challenges.txt (module that contains the problem I faced and how I solved them)
