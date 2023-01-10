
# Vania Art Studio

Vania Art Studio is an E-Commerce Django application about handmade products.  
The application is deployed on Heroku - https://vania-art-studio.herokuapp.com

## Installation

To start the application, recent versions of Python and Django will be needed.
All the required dependencies are located in ```requirements.txt ```



    
## Usage/Examples

### Non-authenticated user

A not logged-in user can only make GET requests and one 
POST request upon valid registration and has only view
permissions.

#### GET requests:

Form for searching specific products: <br>
<img src="https://res.cloudinary.com/hhmf7fxle/image/upload/v1671407568/search_box_iyseya.png" width="300" height="60" />

Forms for filtering the products or change their visualisation:

<img src="https://res.cloudinary.com/hhmf7fxle/image/upload/v1671407569/filter_forms_gidlb5.png" width="600" height="60" />

Form for sorting comments (if any):

<img src="https://res.cloudinary.com/hhmf7fxle/image/upload/v1671407568/comments_form_wzzstf.png" width="250" height="65" />



### Authenticated user
There are 3 types of authenticated users:

#### Base user
<i>Credentials: username - Stamat; password - 12345678stamo </i>   

Base users are allowed to buy products and can make additional 3 POST requests - adding a new comment, edit/delete their own comment and editing their profile data.  

#### Staff user
<i>Credentials: username - Plamen; password - 12345678p </i>  

Except adding new comments and editing profile data, staff users are allowed to create and add new products. When a staff user is authenticated, a new button
will appear on the navigation bar, allowing a new product to be added. Every staff user is able to edit/delete their own products.


#### Admin user

Admin users have full CRUD permissions on every content no matter if they are the creators of the content or not.
