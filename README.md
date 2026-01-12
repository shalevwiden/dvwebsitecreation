## Course Scraping and Data file making

This started as notes for UT only and now its the README for the system I have developed for all schools.

So it seems that .select() and .select_one() are way better for scraping.
<br>
I could and should create a seperate file for excel generation.

---

Descendant (space) → "div p" means: any <p> inside a <div> (at any depth)

Direct child (>) → "div > p" means: only <p> immediately inside <div> (not nested further down)

Ok I guess what can go in each csv and table is the coursecode, coursename, hours, and upper/lower div status.

I moved the JSON path to the init in the class

### Sep 1st, 2025

What I dont need is a new function for each, all I need is a new config, which I can keep in a json file hahaha.
Dope.

Definitely make a SAAS out of this I'm not even gonna lie.

The Excel stuff has succesfully been fully completed.
Now I have to draw a mermaid diagram about it.

I now need to take all this Excel stuff and do it for Rice too lolz...

### Dec 21, 2025

The makedatafiles.py code is gonna be used to standardize school making.

### Dec 23

So I'm gonna do getting the department name stuff here.
In each schools folder there does need to be "departmentname.py" folder.

Ok so this line`departmentname=departmentname.replace('/','_')` is actually required
no matter where you are.

Whenever I want to change a departmentname or such on the deployed website, I'll need to change the departmentname.py of the respective university.

### Getting University stats

I have universitystatsjson.json
I need to add more data to it like the number of departments, biggest department, and smallest department by course amount.
Then I need to make an HTML template which takes the universitystatsjson as arguments and renders it.

I am going to add how many departments there are right now.
Getting the biggest and smallest departments in each school is something you can do in many different ways.

added get_departmentcount() in getunidata() in makedatafiles.py
makedatafiles.py also has to work across schools.

Now working on get_ordered_departmentlist()

### Dec 25, 2025

I wanna do many things today
First one is write the 3 smallest and 3 largest departments from sorteddepartments_json.json to universitystatsjson.json

then I also wanna make this a function in the init
`.replace('-','_').replace(',','_').replace('&','and').replace("'","")`
its a function to get the table name in the databases from the departmentnamecleaned

To make DegreeView, I am using the catalogData class as well as the createUniversity class
self.assetspath (from catalogData) and self.asset_folder_path (from createUniversity) basically refer to the same thing.

### Dec 29, 2025

Similarly to createuniversity, there needs to be a file that calls all instances of the catalogData class

Perhaps they can both be called in the same file since they may use similar arguments, say assets folder, university name and abreviation
Thats probably the best idea

So many paths to keep track of in this project.

For the departmentname.py, I want the class to automatically look for a file named departmentname.py and use it to create the departmentname clean and display departmentname and all that.

### Jan 4, 2026

So in the init of the class Im importing all the code I need in each folder.
The catalogData class is getting much better

Next I need to fix the Excel stuff
Which there was a way I made it much better in my excel project stuff
From Sep 25
Excel Animations lmao

### Jan 6, 2025

Working on Excel stuff
Adding more comments too.
So for each school scraping folder I should include an init.py as well

Added random department.
Can be used for some stuff
`self.random_dept=list(self.jsondata)[random.randint(0,length-1)]`

This removes all tracked stuff
Then readds it

### Jan 11, 2026

I guess I need a way to pass in a custom Excel theme for each school
Make it difference for each instance of the class
Also make it scalable
Like let me pass in a list of excel configs, which is a list
of json paths lets say
I'll include all the Excel configs IN THIS VERY FOLDER
So the paths can be relative
Pass in that list of Excel configs
Then use it in the Excel generation function to generate as many themes as I pass in
Use this same logic for the original UT degree plans.
