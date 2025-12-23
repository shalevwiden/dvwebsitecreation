## UT Austin Course Scraping

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
