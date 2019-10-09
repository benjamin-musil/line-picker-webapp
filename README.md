# Line Picker
https://apt-line-picker.appspot.com/ <br>
APT-Team-6<br>
<i>Team members: Robin Franklin, Nathan Wiatrek, Ben Musil, and Sanjai Pillai</i>

## Table of Contents
[Program Overview](#overview)<br>
[Phase 1](#phase-1)<br>
[Phase 2](#phase-2)<br>

## <a name="overview">Program Overview</a>
<b>Line Checker</b> uses crowdsourcing data to find out wait times of nearby restaurants based on category of food,
distance to user, favorite category set by user, and other similar criteria. Users can submit wait times for specific restaurants with a picture to show the activity of the restaurant. Users also have the ability to add restaurants and check previous post history.

Data is hosted with MangoDB and Flask is used as the web framework to interact between the user and the database.

## <a name="phase-1">Phase 1</a>
### APIs IMPLEMENTED
  1) Create user and post to database
  2) Get user from database based on username
  3) Delete user from database based on username
  4) Get all restaurants from database and list them
  5) Get all restaurants from database by tag and list them
  6) Get wait time by a specific restaurant from database and list them
  
### HOW TO RUN FOR PHASE 1
  1) Run the Flask framework by running the app.py script first
  2) Test API methods by running tests/test_app.py next
  
### RUNNING UNIT TESTS
  1) In pycharm go to the unit test file (these are located in /tests) and run the main method
  2) If you are not in pycharm, simply run `python tests/test_restaurant.py` to run the unit tests for that file

## <a name="phase-2">Phase 2</a>
### Web APIs and How to Access Them
1. <b>Management</b>  
  After logging in using Google's authentication service, the user can change their favorite restaurant under the user settings             page. This will change what restaurants the user sees automatically populated on their home page. Users can also view all their reports under "My Submissions" on the sidebar.

2. <b>Create a Theme</b>  
  Users can create a restaurant by going to "Add a Restaurant" on the sidebar and submitting the requested information.
  
3. <b>View a Theme</b>  
  Users can see restaurant details by clicking on the name of the restaurant that is in the search results field in the "Search Restaurant" section of the site.
  
4. <b>Submit Report</b>  
  Users can submit wait times and images by going to a restaurant page (explained by the View a Theme API) and submitting the requested information.
  
5. <b>View All Themes</b>  
  Users can view see all restaurants at once by clicking the "All" category under "Food Type" in the search page. The search returns title, address, wait time, last reported by, and latest posted image.
  
6. <b>Search Reports</b>  
  Search for a specific restaurant or category by using the search bar on the search page. The searched word will match with tags from either a restaurant name or a category and return matches to the results table.

