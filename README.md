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
