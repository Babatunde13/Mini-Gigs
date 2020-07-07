'''Module used for extra functions that are used in the routes module.'''

#local import
from app import mail, app # imports the Flask Mail and Flask App instance from the __init__ module

def send_mail(user, template, subject, exp=None, **kwargs):
    '''
        Helper function for sending mail
        Args:
            user:---> type: User, the receiver of the mail
            template: string, the html file name that contains the mail
            subject: string, subject of the mail
            exp: time taken for token to expire, if None token doesn't expire
        
        function doesn't return anything, just send mail
    
    '''
    from flask import render_template # For rendering html files
    from flask_mail import Message # imports the function that connects the mail to the server.
    token=user.get_reset_token(expires_sec=exp)
    msg=Message(sender=app.config['MAIL_USERNAME'],
                recipients=[user.email],
                html=render_template(template, token=token, user=user),
                subject=app.config['MAIL_SUBJECT']+ ' - ' +subject)
    mail.send(msg)

def save_pic(image, save_path):
    '''
    Function used to get image data, saves it to a file path and returns the new 
    filename(randomly generated to avoid collision)
    Args:
        image: type: File object.The image to store to a file path and generate a new name for it
        save_path: type: str. Path/directory to save the image

    Returns: the randomly generated file name, name is generated randomly to avoid collision
    '''
    import secrets, os # modules for random tokens and working with directories and files
    from PIL import Image # object used to deal with image
    file_name = secrets.token_hex(8) +os.path.splitext(image.filename)[1]
    file_path = os.path.join(app.root_path, save_path, file_name)
    if save_path == 'static/profileimages':
        image = Image.open(image)
        image.thumbnail((150, 150))
    image.save(file_path)
    return file_name