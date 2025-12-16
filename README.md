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
What I plan to add to
