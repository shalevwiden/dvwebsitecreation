## Creating Degree View Website

Build out each schoolpage and then also each degree page. Put the assets on each of those pages.

This folder also has a virtual environment, which google cloud is installed on, needed for uploading files to the bucket.

DV_Website_Virtual is the virtual environment being used essentially.
It has the google cloud python library to upload files with functions.

Here I use a class with init, then a createschoolpages() function, upload files to cloud function, and a create degree pagaes function.

### Nov 21

Ok so lots to do.
Create fully functional Jinja templates almost every page.

It would be cool to have an interactive timeline on the about DegreeView page.

like a custom stats page for each school.
And of course the course data pages need to be templatized.

I also need to create a fully seperate Excel templates page for the UT site.
Which will host like 260 Excel files.

5 a week for a year.

### Nov 30

Ok lets make the course data pages into templates now.

### Dec 16

Theres a lot that needs to be done:

1. Making the stats page for each school into a template.
   Then adding a method onto the createUniversity class that creates/updates the stats page for each school, with colors and data.
2. In the Jinja, I need to set default values for everything using || because I might add more stuff to the json later.
3. Make a new home page that supports multiple schools.
4. Make a legacy Excel templates page which and a "schoolname" excel page.
   The schoolname excel page will simply show the schools excel template and actually include the JSON file that created it.
5. No new features until launch, so I'm not gonna do this yet, but I wanna add multiple animations to the tables
6. I also wanna add a button to make the table of courses only if it has the department name in the course name.

I should also make the degreeplan files into a template.
What I plan to add to.

When I create all the pages for a school, its gonna do in the "departments" folder.
Then eventually it needs to go in a "Blurbs" folder.
<br>
I need to create a JSON of all the DEGREEVIEW (html) website pages which will go into the random page button creation stuff
I need to use styling thats a folder above all the schools so all the schools can share the same scss obviously.
<br>
<br>
Another change I wanna make:
making the course data page just have it all with dividing it into "A departments, B..." with different subpages.
those A B etc pages can be used when we divide it up by States on the homepage.

<br>
The set up truly is so much work.
But I think once I get the set up right, I can expand to new schools like crazy.

### Dec 17

In createpages.py, Im gonna use in file python dictionaries instead of JSON for now, because Im still establishing exactly what arguments the createUniversity class in createuniversity.py will take.

renamed "createwebsite.py" to "utdegreeplans.py" . This was the file that created the first version of DegreeView with UT Austin degree plans.

### Dec 18

Having ideas for how to do the random page button better.
Instead of having all the links in one js file, put all the links in a json and read it in the js file.
Standardize the name of the json. I should use the school abbreviation, so ut would be like `ut_dv_links.json`. Put it in an html element with display none and get it by id in js.

The element would go in the school page template.

Also I need to put the footer stuff inside the templates folder and also...standardize it.

**dealing with css is a whole nother issue**
I need to make a main.scss and just compile everything to that.
For both legacy DegreeView and the new stuff.
Legacy much later tho.

Inside the createPages class, instead of manually writing out all methods from the createUniversity class that need to be called, I should instead just make a function that does it and calls them. For schools I want to do manually I can just delete that call and write them manually.

Since Im usin Jinja for a lot of template rendering I have to pay attention to where all the paths are.

---

In the actual pages on the site, all the styling should be from a main.css.
Then I can simply ensure its linked correctly when generating the templates.

I need to scss-ize like all the styling for DegreeView for sure lmao.
Untangling the styling is gonna be tricky...

**Ok big progess**
Dec 18th is when I finally generated a poorly done, yet existing, full html department pages for another school besides UT (Rice University).
I guess I gotta pull an all nighter to work on this.

Using a custom ID on each site container, I can divide up the styling into their own scss files, but compile them all to one main.css

All I have to do to make it scalable to all schools is:
Finish the create university class.
Design new homepage.

### Dec 21

I should make a way to have specific code for getting the displaydepartmentname and departmentname half variable across schools, becuase it can vary.
UT has the department code and name seperated by a hyphen.

"GRG - Geography"

While Rice has the department code at the end, in parenthesesis:
Astronomy (ASTR)
All that needs to be done for each school is to get the two needed displaydepartmentname and departmentname half variables.

---

Ok so now I'm thinking just use that code in the generation of the json for every department and just include them as variables at the top.
Ok theres a 3rd one I need to include, departmentname cleaned.

- No slahes
- use "-" instead of slashes or commas

Createuniversity.py is gonna get a lot cleaner once all of those variables are standardized and in the init.

### Dec 25, 2025

Today I am working on getting data from the "universitywidefolder"
and rendering it onto templates

Made the "sorteddepartments_page.html" template in templates

I should make it a convention to call the dictionary I pass into a template
"template data", no matter what.

For the sorteddepartments_page I thought about making a csv but, I'm just gonna make the table copyable.
This means people can easily make a CSV from it if they so choose.

The scss is a whole nother thing...
All of the updated scss is actually in testsite rn
Just need to edit the template that I copy pasted from dvdeployed

I should also make some universal scss partials like "abovemainsite"
"mainsite"
"undermainsite"

### Jan 3, 2026

Goal: make the site scalable befor Jan 11, 2026
Then just expand it all of 2026
Make a big, yet simple, project

What to do now:
update the generation logic because the site path I'm passing in is not departments folder by default
since we are generating school level stuff

Also had the idea on the schools home page to add a random button
that takes you to a random REAL departments page

Ok SCSS is tricky
This probably isnt the greatest way to proceed
But for each scss file I'm gonna put an id for the site container
And then just make the scss for that page (like department page) only apply to that ID

Ok do Stats page
Do home page

Do main main homepage and statspage

Then boom launch
